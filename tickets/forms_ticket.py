from django import forms
from .models import Ticket

class FormulaireTicket(forms.ModelForm):
    message = forms.CharField(label="Message du ticket", widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Votre message initial..."}))
    telephone_demandeur = forms.CharField(
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numéro de téléphone"}),
        max_length=15,
    )

    class Meta:
        model = Ticket
        fields = ["titre", "objet", "priorite", "entreprise", "nom_demandeur", "email_demandeur", "telephone_demandeur"]
        labels = {
            "titre": "Titre du ticket",
            "objet": "Objet du ticket",
            "priorite": "Priorité",
            "entreprise": "Entreprise",
            "nom_demandeur": "Nom du demandeur",
            "email_demandeur": "Email du demandeur",
        }
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre du ticket"}),
            "objet": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Sujet du ticket..."}),
            "priorite": forms.Select(attrs={"class": "form-select"}),
            "entreprise": forms.TextInput(attrs={"class": "form-control", "placeholder": "Entreprise"}),
            "nom_demandeur": forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre nom"}),
            "email_demandeur": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Votre email"}),
        }
