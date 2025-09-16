"""
Fichier views.py : vues principales du projet Ticketing
Commentaires pédagogiques pour étudiant R&T
Chaque vue est expliquée pour faciliter la compréhension du fonctionnement Django
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
import datetime
from .models import Ticket, Message
from .forms import FormulaireInscription
from .forms_ticket import FormulaireTicket
from .forms_message import FormulaireMessage
from django.contrib.auth.models import User

# Vue pour clôturer un ticket
@login_required
def cloturer_ticket(request, ticket_id):
	"""
	Permet à un technicien ou un administrateur de clôturer un ticket.
	Change le statut et la date de résolution.
	"""
	user = request.user
	ticket = Ticket.objects.get(id=ticket_id)
	est_technicien = (ticket.technicien == user and user.groups.filter(name="Technicien").exists())
	est_admin = user.groups.filter(name="Administrateur").exists()
	if est_technicien or est_admin:
		ticket.statut = "resolu"
		ticket.date_resolution = timezone.now()
		ticket.save()
		messages.success(request, "Ticket clôturé avec succès !")
	else:
		messages.error(request, "Vous n'avez pas le droit de clôturer ce ticket.")
	return redirect("detail_ticket", ticket_id=ticket.id)

# Vue pour afficher l'espace technicien
@login_required
def espace_technicien(request):
	"""
	Affiche la liste des tickets à traiter pour les techniciens et administrateurs.
	Permet la recherche et le filtrage.
	"""
	
	user = request.user
	if not user.groups.filter(name__in=["Technicien", "Administrateur"]).exists():
		messages.error(request, "Accès réservé aux techniciens.")
		return redirect("espace_utilisateur")

	q = request.GET.get('q', '').strip()
	# Tickets non attribués
	tickets_attente = Ticket.objects.filter(technicien__isnull=True, statut__in=["nouveau", "en_cours"]).order_by("date_creation")
	tickets_en_cours = Ticket.objects.filter(technicien=user, statut="en_cours").order_by("date_creation")
	tickets_resolus = Ticket.objects.filter(technicien=user, statut="resolu").order_by("date_creation")

	# Recherche par numéro ou mot-clé
	if q:
		if q.isdigit():
			tickets_attente = tickets_attente.filter(id=int(q))
			tickets_en_cours = tickets_en_cours.filter(id=int(q))
			tickets_resolus = tickets_resolus.filter(id=int(q))
		else:
			tickets_attente = tickets_attente.filter(
				models.Q(titre__icontains=q) |
				models.Q(objet__icontains=q) |  # Remplace description__icontains par objet__icontains
				models.Q(entreprise__icontains=q)
			)
			tickets_en_cours = tickets_en_cours.filter(
				models.Q(titre__icontains=q) |
				models.Q(objet__icontains=q) |  # Remplace description__icontains par objet__icontains
				models.Q(entreprise__icontains=q)
			)
			tickets_resolus = tickets_resolus.filter(
				models.Q(titre__icontains=q) |
				models.Q(objet__icontains=q) |  # Remplace description__icontains par objet__icontains
				models.Q(entreprise__icontains=q)
			)

	# Fonction pour déterminer le tag de réponse
	def tag_reponse(ticket):
		"""
		Retourne le type de dernière réponse pour affichage (technicien, utilisateur, nouveau).
		"""
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
	"""
	Permet à un technicien ou administrateur de s'attribuer un ticket non attribué.
	Change le statut à "en cours".
	"""
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
    """
    Affiche le détail d'un ticket et la discussion associée.
    Permet d'ajouter un message si l'utilisateur est concerné.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    utilisateurs = User.objects.filter(groups__name__in=["Technicien", "Administrateur"])
    is_admin_or_technicien = request.user.groups.filter(name__in=["Administrateur", "Technicien"]).exists()
    return render(request, "tickets/detail_ticket.html", {
        "ticket": ticket,
        "utilisateurs": utilisateurs,
        "is_admin_or_technicien": is_admin_or_technicien,
    })

# Vue espace utilisateur
@login_required
def espace_utilisateur(request):
	"""
	Affiche l'espace utilisateur avec la liste de ses tickets.
	Permet la recherche par numéro ou mot-clé.
	"""
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
	"""
	Permet à un utilisateur ou technicien de créer un ticket.
	Enregistre le ticket et le premier message associé.
	"""
	user = request.user
	if not user.groups.filter(name__in=["Utilisateur", "Technicien"]).exists():
		messages.error(request, "Accès réservé aux utilisateurs et techniciens.")
		return redirect("espace_utilisateur")
	if request.method == "POST":
		form = FormulaireTicket(request.POST)
		if form.is_valid():
			ticket = form.save(commit=False)
			ticket.utilisateur = user
			ticket.save()
			# Créer le premier message lié au ticket
			message_texte = form.cleaned_data.get("message")
			if message_texte:
				Message.objects.create(ticket=ticket, auteur=user, texte=message_texte)
			messages.success(request, "Ticket créé avec succès !")
			return redirect("espace_utilisateur")
	else:
		form = FormulaireTicket()
	return render(request, "tickets/creer_ticket.html", {"form": form})

def connexion(request):
	"""
	Vue de connexion utilisateur : vérifie les identifiants et redirige selon le groupe.
	"""
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
	"""
	Vue d'inscription utilisateur : crée un nouveau compte et redirige vers la connexion.
	"""
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
	"""
	Déconnecte l'utilisateur et le redirige vers la page de connexion.
	"""
	logout(request)
	return redirect('connexion')

def statistiques(request):
    """
    Vue statistiques : affiche des indicateurs et graphiques sur les tickets.
    Accessible uniquement aux techniciens et administrateurs.
    """
    user = request.user
    # Seuls admin et technicien peuvent accéder
    if not user.groups.filter(name__in=["Administrateur", "Technicien"]).exists():
        return redirect("espace_utilisateur")

    # Calcul des statistiques
    tickets_ouverts = Ticket.objects.filter(statut__in=["nouveau", "en_cours"]).count()
    tickets_fermes = Ticket.objects.filter(statut="resolu").count()
    tickets_attente = Ticket.objects.filter(statut="nouveau").count()
    tickets_urgents = Ticket.objects.filter(priorite="haute").count()

    # Données pour le graphique tickets par statut
    stat_labels = ["Ouverts", "Fermés", "En attente"]
    stat_counts = [tickets_ouverts, tickets_fermes, tickets_attente]

    # Données pour le graphique tickets par technicien
    tickets_par_technicien = Ticket.objects.values("technicien__username").annotate(total=Count("id")).order_by("-total")
    tech_labels = [t["technicien__username"] or "Non attribué" for t in tickets_par_technicien]
    tech_counts = [t["total"] for t in tickets_par_technicien]

    # Données pour l'évolution mensuelle
    now = timezone.now()
    month_labels = []
    month_counts = []
    for i in range(11, -1, -1):
        month = (now - datetime.timedelta(days=30 * i)).replace(day=1)
        month_labels.append(month.strftime('%b %Y'))
        count = Ticket.objects.filter(date_creation__year=month.year, date_creation__month=month.month).count()
        month_counts.append(count)

    return render(request, "tickets/statistiques.html", {
        "stats": {
            "ouverts": tickets_ouverts,
            "fermes": tickets_fermes,
            "attente": tickets_attente,
            "urgents": tickets_urgents,
        },
        "stat_labels": stat_labels,
        "stat_counts": stat_counts,
        "tech_labels": tech_labels,
        "tech_counts": tech_counts,
        "month_labels": month_labels,
        "month_counts": month_counts,
    })

@login_required
def reattribuer_ticket(request, ticket_id):
    """
    Réattribue un ticket à un autre technicien ou administrateur.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        nouveau_technicien_id = request.POST.get("nouveau_technicien")
        if not nouveau_technicien_id:
            messages.error(request, "Veuillez sélectionner un utilisateur.")
            return redirect("detail_ticket", ticket_id=ticket.id)

        utilisateur = get_object_or_404(User, id=nouveau_technicien_id)

        # Vérifie que l'utilisateur est un technicien ou administrateur
        if not utilisateur.groups.filter(name__in=["Technicien", "Administrateur"]).exists():
            messages.error(request, "L'utilisateur sélectionné n'est pas un technicien ou administrateur.")
            return redirect("detail_ticket", ticket_id=ticket.id)

        # Réattribue le ticket
        ticket.technicien = utilisateur if utilisateur.groups.filter(name="Technicien").exists() else None
        ticket.statut = "nouveau" if utilisateur.groups.filter(name="Administrateur").exists() else "en_cours"
        ticket.save()

        messages.success(request, f"Le ticket a été réattribué à {utilisateur.username}.")
        return redirect("detail_ticket", ticket_id=ticket.id)

    return redirect("detail_ticket", ticket_id=ticket.id)
