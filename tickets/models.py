from django.db import models

class Ticket(models.Model):
	titre = models.CharField(max_length=200)
	objet = models.TextField()
	statut = models.CharField(max_length=50, choices=[
		('nouveau', 'Nouveau'),
		('en_cours', 'En cours'),
		('resolu', 'Résolu'),
	], default='nouveau')
	priorite = models.CharField(max_length=20, choices=[
		('basse', 'Basse'),
		('moyenne', 'Moyenne'),
		('haute', 'Haute'),
	], default='moyenne')
	date_creation = models.DateTimeField(auto_now_add=True)
	date_resolution = models.DateTimeField(null=True, blank=True)
	utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tickets_utilisateur')
	technicien = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_technicien')

	entreprise = models.CharField(max_length=100)
	nom_demandeur = models.CharField(max_length=100, blank=True, null=True)
	email_demandeur = models.EmailField(blank=True, null=True)
	telephone_demandeur = models.CharField(max_length=15, blank=False, null=False, default="0000000000")  # Nouveau champ

	def __str__(self):
		return f"{self.titre} ({self.entreprise})"


class Message(models.Model):
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
	auteur = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	texte = models.TextField()
	date_envoi = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Message de {self.auteur.username} le {self.date_envoi.strftime('%d/%m/%Y %H:%M')}"
