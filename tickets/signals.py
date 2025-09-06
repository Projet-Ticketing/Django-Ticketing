from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def ajouter_au_groupe_utilisateur(sender, instance, created, **kwargs):
    if created:
        groupe, _ = Group.objects.get_or_create(name='Utilisateur')
        instance.groups.add(groupe)
