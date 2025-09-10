"""
Fichier forms_message.py : formulaire pour ajouter un message à un ticket
Commentaires pédagogiques pour étudiant R&T
"""
from django import forms
from .models import Message

class FormulaireMessage(forms.ModelForm):
    class Meta:
        model = Message
        # Un seul champ : le texte du message
        fields = ["texte"]
        labels = {
            "texte": "Votre message",
        }
        widgets = {
            # Widget personnalisé pour le textarea
            "texte": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Votre message...",
                "style": "border-radius:0.5rem; background:#fff; border:1px solid #CBD5E1; font-size:1.05rem;"
            })
        }
