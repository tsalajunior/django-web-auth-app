# Utiliser une image officielle Python
FROM python:3.11-slim

# Empêcher Python d'écrire des fichiers .pyc et d'mettre le buffer sur les logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires (notamment pour PostgreSQL et Pillow)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer les requirements
# UPGRADE_PIP=True
RUN pip install --no-cache-dir --upgrade pip

# Copier le fichier des dépendances
COPY requirements.txt /app/

# Installer les packages Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . /app/