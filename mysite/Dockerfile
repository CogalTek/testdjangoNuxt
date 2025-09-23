# Étape Django simple
FROM python:3.12-slim AS django

WORKDIR /app

# Copier seulement le nécessaire au début (optimise le cache)
COPY mysite/requirements.txt /app/mysite/requirements.txt

# Installer dépendances Python
RUN pip install --no-cache-dir -r mysite/requirements.txt

# Copier tout ton projet
COPY . /app

EXPOSE 8000

CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
