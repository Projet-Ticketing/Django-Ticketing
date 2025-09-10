
from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

# Création automatique des groupes après migration
@receiver(post_migrate)
def create_groups(sender, **kwargs):
    groupes = ['Administrateur', 'Technicien', 'Utilisateur', 'Rapporteur']
    for nom in groupes:
        Group.objects.get_or_create(name=nom)

# Ajout automatique des nouveaux utilisateurs au groupe "Utilisateur"
@receiver(post_save, sender=User)
def ajouter_au_groupe_utilisateur(sender, instance, created, **kwargs):
    if created:
        groupe, _ = Group.objects.get_or_create(name='Utilisateur')
        instance.groups.add(groupe)
