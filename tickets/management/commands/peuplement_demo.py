from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from tickets.models import Ticket, Message
import random
from faker import Faker

class Command(BaseCommand):
    help = "Réinitialise et génère des utilisateurs, techniciens, tickets et messages factices."

    def handle(self, *args, **options):
        fake = Faker('fr_FR')
        # Suppression des anciennes données
        Message.objects.all().delete()
        Ticket.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        # Groupes
        groupes = {
            'Administrateur': Group.objects.get_or_create(name='Administrateur')[0],
            'Technicien': Group.objects.get_or_create(name='Technicien')[0],
            'Utilisateur': Group.objects.get_or_create(name='Utilisateur')[0],
            'Rapporteur': Group.objects.get_or_create(name='Rapporteur')[0],
        }

        # Utilisateurs
        users = []
        for i in range(5):
            username = f"client{i+1}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"client{i+1}@exemple.com",
                    password="test1234"
                )
                user.groups.add(groupes['Utilisateur'])
                users.append(user)
        for i in range(3):
            username = f"tech{i+1}"
            if not User.objects.filter(username=username).exists():
                tech = User.objects.create_user(
                    username=username,
                    email=f"tech{i+1}@exemple.com",
                    password="test1234"
                )
                tech.groups.add(groupes['Technicien'])
                users.append(tech)
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_user(
                username="admin",
                email="admin@exemple.com",
                password="test1234"
            )
            admin.groups.add(groupes['Administrateur'])
            users.append(admin)
        else:
            admin = User.objects.get(username="admin")
            users.append(admin)

        # Tickets
        statuts = ['nouveau', 'en_cours', 'resolu']
        priorites = ['basse', 'moyenne', 'haute']
        entreprises = [fake.company() for _ in range(5)]
        from django.utils import timezone
        import datetime
        for i in range(20):
            utilisateur = random.choice([u for u in users if u.groups.filter(name='Utilisateur').exists()])
            technicien = random.choice([u for u in users if u.groups.filter(name='Technicien').exists()]) if random.random() > 0.5 else None
            statut = random.choice(statuts)
            # Date aléatoire sur l'année écoulée
            days_ago = random.randint(0, 364)
            date_creation = timezone.now() - datetime.timedelta(days=days_ago)
            ticket = Ticket.objects.create(
                titre=fake.sentence(nb_words=6),
                objet=fake.text(max_nb_chars=120),
                statut=statut,
                priorite=random.choice(priorites),
                entreprise=random.choice(entreprises),
                utilisateur=utilisateur,
                technicien=technicien,
                nom_demandeur=utilisateur.username,
                email_demandeur=utilisateur.email,
            )
            # Si on veut fixer une date de création passée malgré auto_now_add,
            # on l'assigne ensuite et on sauvegarde.
            ticket.date_creation = date_creation
            ticket.save(update_fields=['date_creation'])
            # Messages
            for _ in range(random.randint(1, 3)):
                auteur = random.choice([utilisateur, technicien] if technicien else [utilisateur])
                Message.objects.create(
                    ticket=ticket,
                    auteur=auteur,
                    texte=fake.sentence(nb_words=12)
                )
        self.stdout.write(self.style.SUCCESS('Données factices créées avec succès !'))
