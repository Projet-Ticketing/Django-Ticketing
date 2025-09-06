from django import forms
from django.contrib.auth.models import User

class FormulaireInscription(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = User
        fields = ["username", "email", "mot_de_passe"]
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Adresse e-mail",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["mot_de_passe"])
        if commit:
            user.save()
        return user
