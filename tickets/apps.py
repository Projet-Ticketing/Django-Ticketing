from django.apps import AppConfig


class TicketsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'

    def ready(self):
        from django.contrib.auth.models import Group
        groupes = ['Administrateur', 'Technicien', 'Utilisateur', 'Rapporteur']
        for nom in groupes:
            Group.objects.get_or_create(name=nom)
        from . import signals
