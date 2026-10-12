from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Personnalisation de l'affichage du modèle CustomUser dans l'interface d'administration.
    On ajoute nos champs spécifiques dans les sections de visualisation et d'édition.
    """
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'is_staff', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Supplémentaires', {'fields': ('phone_number', 'picture', 'is_verified')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Supplémentaires', {'fields': ('email', 'phone_number', 'picture', 'is_verified')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
