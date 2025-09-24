# ---------- STAGE 1: build Nuxt ----------
FROM node:22-alpine AS build
ARG NuxtAppRoot="app_myFrontendNuxtVue_01"
WORKDIR /app

COPY ${NuxtAppRoot}/package.json ${NuxtAppRoot}/pnpm-lock.yaml* ${NuxtAppRoot}/package-lock.json* ./
RUN npm i

COPY ${NuxtAppRoot}/ ./
RUN npm run generate          # => ./dist

# ---------- STAGE 2: runtime Django ----------
FROM python:3.12-slim AS django
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tini \
 && rm -rf /var/lib/apt/lists/*

# ⬅️ copie Nuxt4
COPY --from=build /app/dist/ ./public/

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
