"""
Fichier forms.py : formulaire d'inscription utilisateur
Commentaires pédagogiques pour étudiant R&T
Chaque champ et méthode est expliqué
"""
from django import forms
from django.contrib.auth.models import User

class FormulaireInscription(forms.ModelForm):
    # Champ mot de passe, affiché comme champ sécurisé
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = User
        # Champs affichés dans le formulaire
        fields = ["username", "email", "mot_de_passe"]
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Adresse e-mail",
        }

    def save(self, commit=True):
        """
        Surcharge la méthode save pour enregistrer le mot de passe de façon sécurisée.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["mot_de_passe"])
        if commit:
            user.save()
        return user
