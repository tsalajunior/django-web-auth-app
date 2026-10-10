from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé qui étant AbstractUser de Django.
    Il intègre les champs de base (username, password, email) 
    et ajoute les spécificités demandées dans le cahier des charges.
    """
    
    # L'email est rendu obligatoire et unique pour permettre l'authentification 
    # et l'envoi du mail de confirmation.
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    
    # Champ pour le numéro de téléphone international 
    # (gère automatiquement le format E.164 grâce à django-phonenumber-field)
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Numéro de téléphone")
    
    # Champ pour la photo de profil (stockée dans le dossier 'profile_pics/')
    # Nécessite la librairie Pillow.
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="Photo de profil")
    
    # Champ pour savoir si l'utilisateur a validé son email via le lien de confirmation
    is_verified = models.BooleanField(default=False, verbose_name="Email vérifié")
    
    # Date et heure de création de compte (générée automatiquement une seule fois à la création)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    # On indique à Django d'utiliser l'email comme identifiant principal pour la connexion 
    # (ou de le garder couplé au username selon ton choix. Ici on garde le username par défaut, 
    # mais l'email devient unique).
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username