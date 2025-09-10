# Plateforme de Ticketing Django

Plateforme de gestion de tickets (helpdesk) en français, avec rôles multiples (Administrateur, Technicien, Utilisateur, Rapporteur), statistiques, recherche, et interface moderne.

## Fonctionnalités
- Création et suivi de tickets
- Messagerie intégrée par ticket
- Statistiques et dashboard
- Gestion des rôles et permissions
- Interface responsive et professionnelle
- Peuplement de données de démonstration

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Projet-Ticketing/Django-Ticketing.git
   cd Django-Ticketing
   ```
2. Créez un environnement virtuel :
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Appliquez les migrations :
   ```bash
   python manage.py migrate
   ```

   Les groupes "Administrateur", "Technicien", "Utilisateur" et "Rapporteur" sont créés automatiquement lors des migrations grâce aux signaux Django.

6. Créez un superutilisateur (admin) pour accéder à l’interface d’administration :
   ```bash
   python manage.py createsuperuser
   ```

7. Lancez le serveur :
   ```bash
   python manage.py runserver
   ```

## Peuplement de données de démo
Pour générer des utilisateurs, tickets et messages fictifs :
```bash
python manage.py peuplement_demo
```

## Utilisation
- Accédez à la page d’accueil pour vous connecter ou vous inscrire.
- Selon votre rôle, accédez à l’espace utilisateur ou technicien.
- Créez, consultez et échangez sur les tickets.
- Visualisez les statistiques et l’évolution des tickets.

## Structure du projet
- `tickets/` : app principale (modèles, vues, templates)
- `plateforme_ticketing/` : configuration Django
- `static/` : fichiers statiques (logo, CSS)
- `requirements.txt` : dépendances Python

## Contributeurs
- Kylian Ascoet
- Sacha Veillon Rodrigues

## Licence
Projet fictif à but pédagogique.
