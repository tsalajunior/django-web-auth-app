# Secure Web Authentication Application

A robust, production-ready Django web authentication application built with modern security standards, containerized with Docker, and backed by PostgreSQL. Designed with strict user session management, real-time email verification, international phone support, and profile customization.

---

## Key Features & Specifications

- **Custom User Model (`CustomUser`)**: Extends Django's AbstractUser to include:
  - International phone number handling (`phonenumber_field`).
  - Profile picture uploads (`ImageField` with local/cloud media storage).
  - Email verification flags (`is_verified`).
- **Secure Authentication Workflow**:
  - Custom user registration with automated email token verification.
  - Strict blocking mechanism: Unverified users cannot log in.
  - Password change management (`PasswordChangeForm`) preserving active sessions (`update_session_auth_hash`).
- **Advanced Security Best Practices**:
  - `@login_required` decorators on protected routes.
  - `@never_cache` decorators on sensitive endpoints to prevent browser history/back-button session leaks after logout.
- **Dockerized Environment**: Fully containerized using Docker Compose with isolated web and database services.

---

## Tech Stack

- **Backend**: Python 3.11, Django 4.2.30
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Production Utilities**: Gunicorn, WhiteNoise, dj-database-url

---

## Project Architecture

```text
web-auth-app/
│
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Global settings (DB, email, media, security)
│   ├── urls.py              # Main URL routing & media serving
│   ├── wsgi.py              # WSGI entry point for production
│   └── asgi.py
│
├── accounts/                # Authentication & user management app
│   ├── migrations/          # Database migrations
│   ├── templates/accounts/  # HTML templates (login, register, profile, main)
│   ├── admin.py             # Custom admin dashboard configuration
│   ├── apps.py
│   ├── forms.py             # Custom creation, update, and password forms
│   ├── models.py            # CustomUser model definition
│   └── views.py             # Authentication & profile views
│
├── media/                   # Uploaded user profile pictures
├── static/                  # Global stylesheets & assets
├── Dockerfile               # Production & dev container configuration
├── docker-compose.yml       # Multi-container orchestration
├── requirements.txt         # Python dependencies
├── Procfile                 # Cloud deployment process file
└── README.md
```

---

## ⚙️ Environment Setup & Local Installation

### Prerequisites

- Install [Docker Desktop](https://www.docker.com/) and ensure it is running.
- Git (optional, for cloning).

### 1. Clone & Navigate to the Project

```bash
cd web-auth-app
```

### 2. Run with Docker Compose

Build and start the services in detached mode:

```bash
docker compose up --build -d
```

### 3. Create a Superuser

To access the Django Administration Dashboard (`http://127.0.0.1:8000/admin/`):

```bash
docker exec -it django_web python manage.py createsuperuser
```

Follow the interactive prompts to set your username, email, and password.

---

## Email Configuration & Testing

The application supports dual email backends:

1. **Development Mode**: Configured to dump verification emails directly into your Docker terminal logs (`console.EmailBackend`).
2. **Production Mode (SMTP/Gmail)**: Uses Google SMTP servers with an App Password.

To configure production Gmail SMTP, add these lines to `config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-google-app-password'
DEFAULT_FROM_EMAIL = 'Your App Name <your-email@gmail.com>'
```

---

## Deployment Guide (Render)

This project is fully optimized for cloud deployment via Docker.

### 1. Required Environment Variables

Set these environment variables on your cloud hosting dashboard:

- `SECRET_KEY`: A secure, random cryptographic string.
- `DEBUG`: Set to `False`.
- `ALLOWED_HOSTS`: Your domain name or cloud provider URL (e.g., `your-app.onrender.com`).
- `DATABASE_URL`: Provided automatically by managed PostgreSQL services (e.g., Render PostgreSQL).

### 2. Static Files & Production Assets

- **WhiteNoise** is integrated into the middleware stack (`config/settings.py`) to serve compressed static files efficiently without requiring an external storage bucket.
- The `Dockerfile` automatically executes `python manage.py collectstatic --noinput` and runs database migrations on container startup.
- **Gunicorn** serves the application via the configured `Procfile`.

```
```
