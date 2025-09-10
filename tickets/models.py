
# Modèles de données pour l'application de ticketing
# Fichier à destination d'un étudiant R&T : chaque champ et méthode est commenté pour faciliter la compréhension.

from django.db import models

class Ticket(models.Model):
	# Titre du ticket (sujet principal)
	titre = models.CharField(max_length=200)
	# Description détaillée du problème ou de la demande
	objet = models.TextField()
	# Statut du ticket (nouveau, en cours, résolu)
	statut = models.CharField(max_length=50, choices=[
		('nouveau', 'Nouveau'),
		('en_cours', 'En cours'),
		('resolu', 'Résolu'),
	], default='nouveau')
	# Priorité du ticket (basse, moyenne, haute)
	priorite = models.CharField(max_length=20, choices=[
		('basse', 'Basse'),
		('moyenne', 'Moyenne'),
		('haute', 'Haute'),
	], default='moyenne')
	# Date de création du ticket (automatique)
	date_creation = models.DateTimeField(auto_now_add=True)
	# Date de résolution du ticket (remplie à la clôture)
	date_resolution = models.DateTimeField(null=True, blank=True)
	# Utilisateur ayant créé le ticket
	utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tickets_utilisateur')
	# Technicien assigné au ticket (peut être nul si non attribué)
	technicien = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_technicien')

	# Entreprise concernée par le ticket
	entreprise = models.CharField(max_length=100)
	# Nom du demandeur (optionnel)
	nom_demandeur = models.CharField(max_length=100, blank=True, null=True)
	# Email du demandeur (optionnel)
	email_demandeur = models.EmailField(blank=True, null=True)
	# Téléphone du demandeur (obligatoire, valeur par défaut si vide)
	telephone_demandeur = models.CharField(max_length=15, blank=False, null=False, default="0000000000")

	def __str__(self):
		"""
		Affiche une représentation lisible du ticket dans l'admin ou le shell.
		"""
		return f"{self.titre} ({self.entreprise})"


class Message(models.Model):
	# Ticket auquel le message est lié
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
	# Auteur du message (utilisateur ou technicien)
	auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	# Contenu du message
	texte = models.TextField()
	# Date d'envoi du message (automatique)
	date_envoi = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""
		Affiche une représentation lisible du message (utile pour debug et admin).
		"""
		return f"Message de {self.auteur.username} le {self.date_envoi.strftime('%d/%m/%Y %H:%M')}"
