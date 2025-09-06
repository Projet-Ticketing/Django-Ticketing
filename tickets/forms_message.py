from django import forms
from .models import Message

class FormulaireMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["texte"]
        labels = {
            "texte": "Votre message",
        }
        widgets = {
            "texte": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Votre message...",
                "style": "border-radius:0.5rem; background:#fff; border:1px solid #CBD5E1; font-size:1.05rem;"
            })
        }
