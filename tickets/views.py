from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import Ticket, Message
from .forms import FormulaireInscription
from .forms_ticket import FormulaireTicket
from .forms_message import FormulaireMessage

# Vue pour clôturer un ticket
@login_required
def cloturer_ticket(request, ticket_id):
	user = request.user
	ticket = Ticket.objects.get(id=ticket_id)
	est_technicien = (ticket.technicien == user and user.groups.filter(name="Technicien").exists())
	est_admin = user.groups.filter(name="Administrateur").exists()
	if est_technicien or est_admin:
		ticket.statut = "resolu"
		from django.utils import timezone
		ticket.date_resolution = timezone.now()
		ticket.save()
		messages.success(request, "Ticket clôturé avec succès !")
	else:
		messages.error(request, "Vous n'avez pas le droit de clôturer ce ticket.")
	return redirect("detail_ticket", ticket_id=ticket.id)

# Vue pour les techniciens : liste des tickets à traiter
@login_required
def espace_technicien(request):
	user = request.user
	if not user.groups.filter(name__in=["Technicien", "Administrateur"]).exists():
		messages.error(request, "Accès réservé aux techniciens.")
		return redirect("espace_utilisateur")

	q = request.GET.get('q', '').strip()
	# Tickets non attribués
	tickets_attente = Ticket.objects.filter(technicien__isnull=True, statut__in=["nouveau", "en_cours"]).order_by("date_creation")
	tickets_en_cours = Ticket.objects.filter(technicien=user, statut="en_cours").order_by("date_creation")
	tickets_resolus = Ticket.objects.filter(technicien=user, statut="resolu").order_by("date_creation")

	if q:
		if q.isdigit():
			tickets_attente = tickets_attente.filter(id=int(q))
			tickets_en_cours = tickets_en_cours.filter(id=int(q))
			tickets_resolus = tickets_resolus.filter(id=int(q))
		else:
			tickets_attente = tickets_attente.filter(
				models.Q(titre__icontains=q) |
				models.Q(description__icontains=q) |
				models.Q(entreprise__icontains=q)
			)
			tickets_en_cours = tickets_en_cours.filter(
				models.Q(titre__icontains=q) |
				models.Q(description__icontains=q) |
				models.Q(entreprise__icontains=q)
			)
			tickets_resolus = tickets_resolus.filter(
				models.Q(titre__icontains=q) |
				models.Q(description__icontains=q) |
				models.Q(entreprise__icontains=q)
			)

	# Fonction pour déterminer le tag de réponse
	def tag_reponse(ticket):
		dernier_message = ticket.messages.order_by('-date_envoi').first()
		if not dernier_message:
			return "Nouveau"
		if dernier_message.auteur == ticket.technicien:
			return "Réponse technicien"
		elif dernier_message.auteur == ticket.utilisateur:
			return "Réponse utilisateur"
		else:
			return "En attente"

	# Ajout du tag à chaque ticket
	for t in list(tickets_attente) + list(tickets_en_cours) + list(tickets_resolus):
		t.tag_reponse = tag_reponse(t)

	tickets_recherche = []
	if q:
		tickets_recherche = list(tickets_attente) + list(tickets_en_cours) + list(tickets_resolus)
	return render(request, "tickets/espace_technicien.html", {
		"tickets_attente": tickets_attente,
		"tickets_en_cours": tickets_en_cours,
		"tickets_resolus": tickets_resolus,
		"tickets_recherche": tickets_recherche,
		"q": q,
	})

# Vue pour qu'un technicien s'attribue un ticket
@login_required
def attribuer_ticket(request, ticket_id):
	user = request.user
	if not user.groups.filter(name__in=["Technicien", "Administrateur"]).exists():
		messages.error(request, "Accès réservé aux techniciens.")
		return redirect("espace_utilisateur")
	ticket = Ticket.objects.get(id=ticket_id)
	if ticket.technicien is None:
		ticket.technicien = user
		ticket.statut = "en_cours"
		ticket.save()
		messages.success(request, "Ticket attribué !")
	else:
		messages.error(request, "Ce ticket est déjà attribué.")
	return redirect("espace_technicien")

# Vue détail ticket avec boîte de dialogue
@login_required
def detail_ticket(request, ticket_id):
	ticket = Ticket.objects.get(id=ticket_id)
	# Vérification que l'utilisateur est concerné
	user = request.user
	est_concerne = (user == ticket.utilisateur) or user.groups.filter(name__in=["Technicien", "Administrateur"]).exists()
	if not est_concerne:
		messages.error(request, "Vous n'avez pas accès à ce ticket.")
		return redirect("espace_utilisateur")
	messages_ticket = ticket.messages.order_by("date_envoi")
	if request.method == "POST":
		form = FormulaireMessage(request.POST)
		if form.is_valid():
			message = form.save(commit=False)
			message.ticket = ticket
			message.auteur = user
			message.save()
			return redirect("detail_ticket", ticket_id=ticket.id)
	else:
		form = FormulaireMessage()
	is_admin = user.groups.filter(name="Administrateur").exists()
	is_technicien = user.groups.filter(name="Technicien").exists()
	return render(
		request,
		"tickets/detail_ticket.html",
		{
			"ticket": ticket,
			"messages_ticket": messages_ticket,
			"form": form,
			"is_admin": is_admin,
			"is_technicien": is_technicien,
		}
	)

# Vue espace utilisateur
@login_required
def espace_utilisateur(request):
	q = request.GET.get('q', '').strip()
	tickets = request.user.tickets_utilisateur.all()
	if q:
		if q.isdigit():
			tickets = tickets.filter(id=int(q))
		else:
			tickets = tickets.filter(
				models.Q(titre__icontains=q) |
				models.Q(description__icontains=q) |
				models.Q(entreprise__icontains=q)
			)
	return render(request, "tickets/espace_utilisateur.html", {"tickets": tickets, "q": q})

# Vue pour la création de ticket
@login_required
def creer_ticket(request):
    if request.method == "POST":
        form = FormulaireTicket(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.utilisateur = request.user
            ticket.save()
            # Créer le premier message lié au ticket
            message_texte = form.cleaned_data.get("message")
            if message_texte:
                Message.objects.create(ticket=ticket, auteur=request.user, texte=message_texte)
            messages.success(request, "Ticket créé avec succès !")
            return redirect("espace_utilisateur")
    else:
        form = FormulaireTicket()
    return render(request, "tickets/creer_ticket.html", {"form": form})

def connexion(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# Redirection selon le groupe
			if user.groups.filter(name__in=["Technicien", "Administrateur"]).exists():
				return redirect("espace_technicien")
			elif user.groups.filter(name="Rapporteur").exists():
				return redirect("espace_utilisateur")
			else:
				return redirect("espace_utilisateur")
		else:
			messages.error(request, "Identifiants invalides.")
	return render(request, "tickets/connexion.html")

def inscription(request):
	if request.method == "POST":
		form = FormulaireInscription(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Votre compte a été créé avec succès !")
			return redirect("connexion")
	else:
		form = FormulaireInscription()
	return render(request, "tickets/inscription.html", {"form": form})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def statistiques(request):
	user = request.user
	# Seuls admin et technicien peuvent accéder
	if not user.groups.filter(name__in=["Administrateur", "Technicien"]).exists():
		return redirect("espace_utilisateur")
	total_tickets = Ticket.objects.count()
	tickets_ouverts = Ticket.objects.filter(statut__in=["nouveau", "en_cours"]).count()
	tickets_resolus = Ticket.objects.filter(statut="resolu").count()
	tickets_en_attente = Ticket.objects.filter(statut="nouveau").count()
	tickets_par_technicien = Ticket.objects.values("technicien__username").annotate(total=Count("id")).order_by("-total")

	# Données pour le graphique tickets par statut
	statuts = ["nouveau", "en_cours", "resolu"]
	stat_labels = ["Nouveau", "En cours", "Résolu"]
	stat_counts = [Ticket.objects.filter(statut=s).count() for s in statuts]

	# Données pour le graphique tickets par technicien
	tech_labels = [t["technicien__username"] or "Non attribué" for t in tickets_par_technicien]
	tech_counts = [t["total"] for t in tickets_par_technicien]

	# Données pour l'évolution mensuelle
	from django.db.models.functions import TruncMonth
	from django.utils import timezone
	import datetime
	now = timezone.now()
	months = []
	month_labels = []
	month_counts = []
	for i in range(11, -1, -1):
		month = (now - datetime.timedelta(days=30*i)).replace(day=1)
		months.append(month)
		month_labels.append(month.strftime('%b %Y'))
	for month in months:
		count = Ticket.objects.filter(date_creation__year=month.year, date_creation__month=month.month).count()
		month_counts.append(count)

	return render(request, "tickets/statistiques.html", {
		"total_tickets": total_tickets,
		"tickets_ouverts": tickets_ouverts,
		"tickets_resolus": tickets_resolus,
		"tickets_en_attente": tickets_en_attente,
		"tickets_par_technicien": tickets_par_technicien,
		"stat_labels": stat_labels,
		"stat_counts": stat_counts,
		"tech_labels": tech_labels,
		"tech_counts": tech_counts,
		"month_labels": month_labels,
		"month_counts": month_counts,
	})
