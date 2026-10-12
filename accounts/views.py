from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# décorateurs nécessaires pour protéger certaines vues et gérer la mise en cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout

from .forms import CustomUserCreationForm, UserUpdateForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import resend

import os

User = get_user_model()


def register_view(request):
    """
    Gère l'inscription de l'utilisateur.
    À la validation du formulaire, le compte est créé (is_verified=False)
    et un email de confirmation est envoyé via Resend.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False  # Pas encore vérifié par email
            user.save()

            # Génération d'un token sécurisé et d'un uid pour le lien de confirmation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Détection dynamique du protocole et du domaine (Localhost vs Render)
            protocol = "https" if request.is_secure() else "http"
            domain = request.get_host()

            # Construction du lien de confirmation dynamique
            confirmation_link = f"{protocol}://{domain}/accounts/verify/{uid}/{token}/"

            # Appel de la fonction d'envoi via Resend
            send_verification_email(user, confirmation_link)

            messages.success(
                request,
                "Inscription réussie ! Un e-mail de confirmation vous a été envoyé.",
            )
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


# Configuration de la clé API Resend (récupérée des variables d'environnement)
resend.api_key = os.environ.get("RESEND_API_KEY")


def verify_email_view(request, uidb64, token):
    """
    Valide l'e-mail de l'utilisateur via le lien reçu,
    passe is_verified à True et redirige vers la connexion.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(
            request,
            "Votre e-mail a été validé avec succès ! Vous pouvez maintenant vous connecter.",
        )
        return redirect("accounts:login")
    else:
        messages.error(request, "Le lien de confirmation est invalide ou a expiré.")
        return redirect("accounts:register")


@never_cache
def login_view(request):
    """
    Gère la connexion de l'utilisateur.
    Vérifie si les identifiants existent et redirige vers la page principale.
    """
    # Si l'utilisateur est déjà connecté, inutile de voir le formulaire de login, on le redirige vers main
    if request.user.is_authenticated:
        return redirect("accounts:main_page")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_verified:
                    messages.error(
                        request,
                        "Veuillez d'abord valider votre e-mail via le lien reçu avant de vous connecter.",
                    )
                    return redirect("accounts:login")
                login(request, user)
                messages.success(request, f"Bienvenue, {username} !")
                return redirect(
                    "accounts:main_page"
                )  # Redirection vers la page principale
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required(login_url="accounts:login")
@never_cache
def main_page_view(request):
    """
    La page principale protégée.
    @login_required : Force l'utilisateur à être connecté.
    @never_cache : Empêche le navigateur de garder cette page en mémoire après déconnexion.
    """
    return render(request, "accounts/main.html")


def logout_view(request):
    """
    Gère la déconnexion propre de l'utilisateur.
    """
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
@never_cache
def profile_view(request):
    """
    Permet à l'utilisateur connecté de voir/modifier ses infos personnelles
    ET de changer son mot de passe sur la même page.
    """
    form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "profile_form":
            form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre profil a été mis à jour avec succès !")
                return redirect("accounts:profile")

        elif form_type == "password_form":
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, "Votre mot de passe a été modifié avec succès !"
                )
                return redirect("accounts:profile")

    context = {
        "form": form,
        "password_form": password_form,
    }
    return render(request, "accounts/profile.html", context)


def send_verification_email(user, verification_link):
    """
    Envoie l'e-mail de validation via l'API HTTP de Resend.
    """
    params = {
        "from": "onboarding@resend.dev",  # Adresse de test par défaut de Resend
        "to": [user.email],
        "subject": "Confirmez votre inscription",
        "html": f"""
            <p>Bonjour {user.username},</p>
            <p>Veuillez cliquer sur le lien suivant pour valider votre inscription :</p>
            <p><a href="{verification_link}">Activer mon compte</a></p>
        """
    }
    try:
        email = resend.Emails.send(params)
        return email
    except Exception as e:
        print(f"Erreur d'envoi d'e-mail via Resend : {e}")
