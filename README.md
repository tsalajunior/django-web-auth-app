# Application d'Authentification Web Sécurisée (Django)

Une application web d'authentification Django robuste et prête pour la production, construite selon les normes de sécurité modernes, conteneurisée avec Docker et alimentée par PostgreSQL. Elle intègre une gestion stricte des sessions utilisateur, une vérification des e-mails en temps réel via l'API Resend, un support des numéros de téléphone internationaux et la personnalisation des profils.

---

## Fonctionnalités Clés & Spécifications

- **Modèle Utilisateur Personnalisé (`CustomUser`)** : Étend le modèle `AbstractUser` de Django pour inclure :
  - La gestion des numéros de téléphone internationaux (`phonenumber_field`).
  - Le téléchargement de photos de profil (`ImageField`).
  - Des indicateurs de vérification des e-mails (`is_verified`).
- **Flux d'Authentification Sécurisé** :
  - Inscription personnalisée avec vérification par jeton unique envoyé par e-mail via l'API Resend.
  - Mécanisme de blocage strict : Les utilisateurs non vérifiés ne peuvent pas se connecter.
  - Gestion du changement de mot de passe (`PasswordChangeForm`) préservant les sessions actives (`update_session_auth_hash`).
- **Bonnes Pratiques de Sécurité Avancées** :
  - Décorateurs `@login_required` sur les routes protégées.
  - Décorateurs `@never_cache` sur les pages sensibles pour empêcher les fuites de session via le bouton "Précédent" du navigateur après une déconnexion.
  - Protection CSRF renforcée pour la production (`CSRF_TRUSTED_ORIGINS`, cookies sécurisés).
- **Environnement Conteneurisé (Docker)** : Entièrement conteneurisé avec Docker Compose pour isoler les services web et de base de données.

---

## Stack Technique

- **Backend** : Python 3.11, Django 4.2.30
- **Base de données** : PostgreSQL
- **Conteneurisation** : Docker & Docker Compose
- **Frontend** : Bootstrap 5, HTML5, CSS3
- **Utilitaires de Production** : Gunicorn, WhiteNoise, API Resend (e-mails transactionnels)

---

## Architecture du Projet

```text
web-auth-app/
│
├── config/                  # Configuration du projet Django
│   ├── __init__.py
│   ├── settings.py          # Paramètres globaux (BDD, sécurité, médias)
│   ├── urls.py              # Routage principal & gestion des médias
│   ├── wsgi.py              # Point d'entrée WSGI pour la production
│   └── asgi.py
│
├── accounts/                # Application d'authentification et gestion des utilisateurs
│   ├── migrations/          # Migrations de la base de données
│   ├── templates/accounts/  # Templates HTML (connexion, inscription, profil, accueil)
│   ├── admin.py             # Configuration du tableau de bord administrateur
│   ├── apps.py
│   ├── forms.py             # Formulaires de création, de mise à jour et de mot de passe
│   ├── models.py            # Définition du modèle CustomUser
│   └── views.py             # Vues d'authentification, de profil et intégration Resend
│
├── media/                   # Photos de profil des utilisateurs
├── static/                  # Feuilles de style et actifs globaux
├── Dockerfile               # Configuration du conteneur (production & dev)
├── docker-compose.yml       # Orchestration multi-conteneurs
├── requirements.txt         # Dépendances Python
├── Procfile                 # Fichier de processus pour le cloud
└── README.md
```

---

## ⚙️ Configuration de l'Environnement & Installation Locale

### Prérequis

- Installer [Docker Desktop](https://www.docker.com/) et s'assurer qu'il est en cours d'exécution.
- Git (pour le clonage).

### 1. Naviguer dans le Projet

```bash
cd web-auth-app
```

### 2. Lancer avec Docker Compose

Construire et démarrer les services en arrière-plan :

```bash
docker compose up --build -d
```

### 3. Créer un Superutilisateur

Pour accéder au tableau de bord d'administration Django (`http://127.0.0.1:8000/admin/`) :

```bash
docker exec -it django_web python manage.py createsuperuser
```

Suivez les instructions interactives pour définir le nom d'utilisateur, l'e-mail et le mot de passe.

---

## Configuration des E-mails & API Transactionnelle (Resend)

L'application utilise une solution d'e-mailing moderne par API pour s'affranchir des limitations SMTP synchrones et éviter les expirations de délais (erreurs 502) sur les hébergements cloud :

- **Mode Développement** : Peut utiliser le backend console pour le débogage local.
- **Mode Production** : S'intègre avec **Resend** via son API HTTP (`paquet python resend`) pour une livraison instantanée et fiable des e-mails de validation.

Assurez-vous que la variable d'environnement `RESEND_API_KEY` est correctement définie.

---

## Guide de Déploiement (Render)

Ce projet est entièrement optimisé pour un déploiement cloud via Docker sur des plateformes telles que Render.

### 1. Variables d'Environnement Requises

Configurez ces variables dans le tableau de bord de votre hébergeur cloud :

- `SECRET_KEY` : Une chaîne cryptographique secrète et aléatoire.
- `DEBUG` : Défini à `False`.
- `ALLOWED_HOSTS` : Votre nom de domaine ou URL de service cloud (ex: `votre-app.onrender.com`).
- `DATABASE_URL` : Fournie automatiquement par les services PostgreSQL managés (ex: Render PostgreSQL).
- `RESEND_API_KEY` : Votre clé API Resend pour l'envoi d'e-mails.

### 2. Fichiers Statiques & Actifs de Production

- **WhiteNoise** est intégré dans la pile middleware (`config/settings.py`) pour servir les fichiers statiques compressés efficacement sans nécessiter de bucket de stockage externe.
- Le `Dockerfile` exécute automatiquement les migrations de base de données, initialise un superutilisateur par défaut si absent, lance `python manage.py collectstatic --noinput` et démarre Gunicorn.
- **Gunicorn** sert l'application via le `Procfile` configuré avec des seuils de délai (timeout) adaptés pour éviter les arrêts brutaux (`SIGKILL`) sur les instances partagées ou gratuites.