"""
Fichier apps.py : configuration de l'application tickets
Commentaires pédagogiques pour étudiant R&T
"""
from django.apps import AppConfig

class TicketsConfig(AppConfig):
    # Définit le type de clé primaire par défaut
    default_auto_field = 'django.db.models.BigAutoField'
    # Nom de l'application (doit correspondre au dossier)
    name = 'tickets'

