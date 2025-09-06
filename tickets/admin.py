from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ('titre', 'statut', 'priorite', 'entreprise', 'date_creation', 'utilisateur')
	search_fields = ('titre', 'description', 'entreprise')
	list_filter = ('statut', 'priorite', 'entreprise')
