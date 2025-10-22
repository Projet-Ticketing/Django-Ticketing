# Plateforme de Ticketing Django

Plateforme de gestion de tickets (helpdesk) en français, avec rôles multiples (Administrateur, Technicien, Utilisateur, Rapporteur), statistiques, recherche, et interface moderne.

## Fonctionnalités
- Création et suivi de tickets
- Messagerie intégrée par ticket
- Statistiques et dashboard
- Gestion des rôles et permissions
- Interface responsive et professionnelle
- Peuplement de données de démonstration

## Commande simplifié et rapide
   ```bash
   git clone https://github.com/Projet-Ticketing/Django-Ticketing.git
   cd Django-Ticketing
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   env/bin/activate && python manage.py makemigrations tickets && python manage.py migrate && python manage.py createsuperuser && python manage.py peuplement_demo
   ```

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

### Créer un superutilisateur (compte admin)
Ce compte permet d'accéder à l'interface d'administration Django :
```bash
python manage.py createsuperuser
```
Suivez les instructions (nom d'utilisateur, email, mot de passe).

### Lancer le serveur de développement
```bash
python manage.py runserver
```
Le site sera accessible à l'adresse http://127.0.0.1:8000 dans votre navigateur.

### Accéder à l'administration Django et gérer les techniciens

Pour accéder à l'interface d'administration Django :
- Ouvrez votre navigateur et allez sur : [http://localhost:8000/admin](http://localhost:8000/admin)
- Connectez-vous avec le compte admin créé à l'étape 6 (`createsuperuser`).

Pour ajouter un technicien :
1. Dans l'admin, créez un nouvel utilisateur (menu Utilisateurs).
2. Cliquez sur l'utilisateur créé pour modifier ses groupes.
3. Ajoutez-le au groupe **Technicien**.
4. Retirez-le du groupe **Utilisateur** si besoin (pour qu'il n'ait que le rôle technicien).

Ainsi, le nouvel utilisateur aura accès à l'espace technicien et pourra gérer les tickets attribués.

### Peupler la base avec des données de démonstration (optionnel)
Pour tester avec des exemples :
```bash
python manage.py peuplement_demo
```

### Utilisation du site
- Rendez-vous sur la page d'accueil pour vous inscrire ou vous connecter.
- Selon votre rôle, accédez à l'espace utilisateur ou technicien.
- Créez, consultez et échangez sur les tickets.
- Visualisez les statistiques et l'évolution des tickets.

### Conseils et dépannage
- Si une commande ne fonctionne pas, vérifiez que vous êtes bien dans le dossier du projet et que l'environnement virtuel est activé.
- Pour toute question, consultez la documentation Django : https://docs.djangoproject.com/fr/5.2/
- En cas de problème de dépendance, relancez `pip install -r requirements.txt`.

---

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
