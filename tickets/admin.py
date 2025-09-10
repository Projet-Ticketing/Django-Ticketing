"""
Fichier admin.py : configuration de l'administration Django pour les tickets
Commentaires pédagogiques pour étudiant R&T
"""
from django.contrib import admin
from .models import Ticket

# Enregistre le modèle Ticket dans l'interface d'administration
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	# Colonnes affichées dans la liste des tickets
	list_display = ('titre', 'statut', 'priorite', 'entreprise', 'date_creation', 'utilisateur')
	# Champs sur lesquels on peut faire une recherche
	search_fields = ('titre', 'description', 'entreprise')
	# Filtres disponibles dans la barre latérale
	list_filter = ('statut', 'priorite', 'entreprise')
