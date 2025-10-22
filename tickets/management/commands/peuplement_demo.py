from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone

from tickets.models import Ticket, Message

import random
import datetime
from faker import Faker


class Command(BaseCommand):
    help = (
        "Réinitialise (wipe) les données de démo puis génère des utilisateurs, "
        "techniciens, tickets et messages factices."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("fr_FR")
        User = get_user_model()

        # --------------------------
        # Wipe des données existantes
        # --------------------------
        self.stdout.write(self.style.WARNING("Suppression des anciennes données…"))
        Message.objects.all().delete()
        Ticket.objects.all().delete()
        # On garde les superusers existants ; on efface le reste
        User.objects.filter(is_superuser=False).delete()

        # --------------------------
        # Groupes requis
        # --------------------------
        groupes = {
            "Administrateur": Group.objects.get_or_create(name="Administrateur")[0],
            "Technicien": Group.objects.get_or_create(name="Technicien")[0],
            "Utilisateur": Group.objects.get_or_create(name="Utilisateur")[0],
            "Rapporteur": Group.objects.get_or_create(name="Rapporteur")[0],
        }

        # --------------------------
        # Utilisateurs de démo
        # --------------------------
        users = []

        # Clients (utilisateurs finaux)
        for i in range(5):
            username = f"client{i+1}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@exemple.com",
                    password="test1234",
                )
                user.groups.add(groupes["Utilisateur"])
                users.append(user)

        # Techniciens
        for i in range(3):
            username = f"tech{i+1}"
            if not User.objects.filter(username=username).exists():
                tech = User.objects.create_user(
                    username=username,
                    email=f"{username}@exemple.com",
                    password="test1234",
                )
                tech.groups.add(groupes["Technicien"])
                users.append(tech)

        # Superuser admin (mdp très faible, seulement pour dev/démo)
        admin_username = "admin"
        admin_password = "admin"
        admin_email = "admin@exemple.com"

        admin_qs = User.objects.filter(username=admin_username)
        if admin_qs.exists():
            admin = admin_qs.first()
            admin.is_superuser = True
            admin.is_staff = True
            admin.email = admin_email
            admin.set_password(admin_password)
            admin.save()
            admin.groups.add(groupes["Administrateur"])
            self.stdout.write(
                self.style.WARNING(
                    "Utilisateur 'admin' mis à jour (superuser + mot de passe réinitialisé)."
                )
            )
        else:
            admin = User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
            )
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            admin.groups.add(groupes["Administrateur"])
            self.stdout.write(
                self.style.WARNING(
                    "Superuser 'admin' créé avec le mot de passe par défaut (admin)."
                )
            )
        users.append(admin)
        self.stdout.write(
            self.style.WARNING(
                "ATTENTION: le mot de passe 'admin' est très faible — usage DEV uniquement."
            )
        )

        # --------------------------
        # Tickets + Messages
        # --------------------------
        statuts = ["nouveau", "en_cours", "resolu"]
        priorites = ["basse", "moyenne", "haute"]
        entreprises = [fake.company() for _ in range(5)]

        # Helpers pour tirage pondéré
        def any_user_in_group(name: str):
            return [u for u in users if u.groups.filter(name=name).exists()]

        utilisateurs_final = any_user_in_group("Utilisateur")
        techniciens = any_user_in_group("Technicien")

        for _ in range(20):
            utilisateur = random.choice(utilisateurs_final)
            technicien = random.choice(techniciens) if techniciens and random.random() > 0.5 else None
            statut = random.choice(statuts)

            # Date aléatoire sur l’année écoulée
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
            # Forcer une date de création passée si le modèle utilise auto_now_add
            ticket.date_creation = date_creation
            ticket.save(update_fields=["date_creation"])

            # Messages (1 à 3)
            nb_messages = random.randint(1, 3)
            for _ in range(nb_messages):
                auteur = random.choice(
                    [utilisateur, technicien] if technicien else [utilisateur]
                )
                Message.objects.create(
                    ticket=ticket,
                    auteur=auteur,
                    texte=fake.sentence(nb_words=12),
                )

        self.stdout.write(self.style.SUCCESS("Données factices créées avec succès."))
