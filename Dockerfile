# ---------- STAGE 1: build des apps Nuxt (uniquement si .nuxt présent) ----------
FROM node:20-bullseye AS nuxt-builder
WORKDIR /app
# Contexte = Nuxt3Test/mysite
COPY . /app

# Parcourt tous les dossiers "app_*" à la racine du contexte (ici ./)
# et build UNIQUEMENT ceux qui contiennent .nuxt/
RUN set -eux; \
    built_any=0; \
    for d in $(find . -maxdepth 1 -type d -name 'app_*'); do \
        echo 
        if [ -d "$d/.nuxt" ]; then \
            echo "📦 Found Nuxt app (has .nuxt): $d"; \
            cd "$d"; \
            if [ -f package-lock.json ]; then npm ci; else npm install; fi; \
            npm run build; \
            cd /app; \
            built_any=1; \
        else \  
            echo "⏭️  Skipping $d (no .nuxt dir)"; \
        fi; \
    done; \
    if [ "$built_any" -eq 0 ]; then \
        echo "ℹ️ No Nuxt apps with '.nuxt' found. Skipping builds."; \
    fi


# ---------- STAGE 2: runtime Django ----------
FROM python:3.12-slim AS django
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates tini \
 && rm -rf /var/lib/apt/lists/*

# Copie tout le projet (inclut les outputs Nuxt du stage précédent)
COPY --from=nuxt-builder /app /app

# ✅ Ici, le requirements.txt est bien à la racine du contexte (Nuxt3Test/mysite/requirements.txt)
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000
ENTRYPOINT ["/usr/bin/tini","--"]
# manage.py est à la racine du contexte -> /app/manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

