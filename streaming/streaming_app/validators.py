from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Le mot de passe doit contenir au moins une majuscule.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Le mot de passe doit contenir au moins une minuscule.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[@$!%*#?&]', password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")

    def get_help_text(self):
        return (
            "Votre mot de passe doit contenir au moins 10 caractères, "
            "avec une majuscule, une minuscule, un chiffre et un caractère spécial."
        )
