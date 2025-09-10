# Plateforme de Ticketing Django

Plateforme de gestion de tickets (helpdesk) en français, avec rôles multiples (Administrateur, Technicien, Utilisateur, Rapporteur), statistiques, recherche, et interface moderne.

## Fonctionnalités
- Création et suivi de tickets
- Messagerie intégrée par ticket
- Statistiques et dashboard
- Gestion des rôles et permissions
- Interface responsive et professionnelle
- Peuplement de données de démonstration

## Procédure d'installation et de lancement (débutant)

### 1. Prérequis
Assurez-vous d'avoir installé :
- **Python 3.10 ou plus** (téléchargeable sur https://www.python.org)
- **Git** (téléchargeable sur https://git-scm.com)

### 2. Cloner le projet
Ouvrez un terminal et tapez :
```bash
git clone https://github.com/Projet-Ticketing/Django-Ticketing.git
cd Django-Ticketing
```

### 3. Créer un environnement virtuel Python
Cela permet d'isoler les dépendances du projet :
```bash
python3 -m venv env
```
Activez l'environnement virtuel :
- Sur **Mac/Linux** :
   ```bash
   source env/bin/activate
   ```
- Sur **Windows** :
   ```bash
   .\env\Scripts\activate
   ```
Vous devriez voir `(env)` devant la ligne de commande.

### 4. Installer les dépendances Python
Installez tous les modules nécessaires :
```bash
pip install -r requirements.txt
```
Si vous avez une erreur, vérifiez que l'environnement virtuel est bien activé.

### 5. Appliquer les migrations (préparer la base de données)
```bash
python manage.py migrate
```

### 6. Créer un superutilisateur (compte admin)
Ce compte permet d'accéder à l'interface d'administration Django :
```bash
python manage.py createsuperuser
```
Suivez les instructions (nom d'utilisateur, email, mot de passe).

### 7. Lancer le serveur de développement
```bash
python manage.py runserver
```
Le site sera accessible à l'adresse http://127.0.0.1:8000 dans votre navigateur.

### 8. Peupler la base avec des données de démonstration (optionnel)
Pour tester avec des exemples :
```bash
python manage.py peuplement_demo
```

### 9. Utilisation du site
- Rendez-vous sur la page d'accueil pour vous inscrire ou vous connecter.
- Selon votre rôle, accédez à l'espace utilisateur ou technicien.
- Créez, consultez et échangez sur les tickets.
- Visualisez les statistiques et l'évolution des tickets.

### 10. Conseils et dépannage
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
