# Utiliser une image officielle Python slim
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Empêcher Python d'écrire des fichiers .pyc et d'activer le mode unbuffered pour les logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances système nécessaires (ex: pour PostgreSQL et compilation)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet dans le conteneur
COPY . .

# Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Commande par défaut pour lancer les migrations, préparer les fichiers statiques et démarrer Gunicorn
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn config.wsgi:application --bind 0.0.0.0:8000