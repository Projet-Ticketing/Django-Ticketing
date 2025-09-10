"""
Fichier signals.py : signaux pour automatiser l'ajout au groupe Utilisateur
Commentaires pédagogiques pour étudiant R&T
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

# Signal appelé à chaque création d'utilisateur
@receiver(post_save, sender=User)
def ajouter_au_groupe_utilisateur(sender, instance, created, **kwargs):
    """
    Ajoute automatiquement tout nouvel utilisateur au groupe 'Utilisateur'.
    Permet de gérer les droits par groupe facilement.
    """
    if created:
        groupe, _ = Group.objects.get_or_create(name='Utilisateur')
        instance.groups.add(groupe)
