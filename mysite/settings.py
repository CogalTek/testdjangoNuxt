# tabs = \t
from pathlib import Path
import os
import json

# --- Base ---
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ecx42b3sk8%lijl^_k1u=^=o^gc)xl99b11!al!$6f%494zt7u'
DEBUG = True
ALLOWED_HOSTS: list[str] = ["*"]  # dev

# --- Apps Django natives ---
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# Production (optionnel) :
	# 'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# --- DB (dev) ---
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

# --- Auth ---
AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- i18n ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# --- Staticfiles ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# évite le warning si "static/" n'existe pas
STATICFILES_DIRS: list[str | os.PathLike] = []
if (BASE_DIR / 'static').exists():
	STATICFILES_DIRS.append(BASE_DIR / 'static')

# --- Détection Nuxt (SPA/SSG) ---
def _discover_nuxt_public_dirs() -> tuple[list[str], list[dict]]:
	apps_public: list[str] = []
	apps_detected: list[dict] = []

	# 1) Détection automatique dans les dossiers app_* (monorepo)
	search_roots = [os.path.abspath(BASE_DIR.parent), str(BASE_DIR)]
	for root in search_roots:
		if not os.path.isdir(root):
			continue
		for entry in os.listdir(root):
			if not entry.startswith("app_"):
				continue
			app_dir = os.path.join(root, entry)
			if not os.path.isdir(app_dir):
				continue

			# Critère simple : build présent => .output/public/index.html
			public_dir = os.path.join(app_dir, ".output", "public")
			is_public = os.path.isfile(os.path.join(public_dir, "index.html"))

			# n'ajoute QUE si c'est vraiment un Nuxt buildé
			if is_public:
				apps_detected.append({
					"name": entry,
					"path": app_dir,
					"type": "nuxt",
					"public": public_dir,
				})
				apps_public.append(public_dir)

	# 2) Manifest optionnel (si écrit par le Dockerfile de build)
	manifest_path = BASE_DIR / "nuxt_apps.json"
	if manifest_path.exists():
		try:
			data = json.loads(manifest_path.read_text())
			for app in data:
				raw_public = Path(app.get("public", ""))
				name = app.get("name", "nuxt-app")

				# Stratégie robuste : si le chemin du manifest n'existe pas en runtime,
				# tente les emplacements classiques copiés par l'image : /app/public puis /app/frontend
				candidates = [raw_public, BASE_DIR / "public", BASE_DIR / "frontend"]
				for cand in candidates:
					if cand and (cand / "index.html").exists():
						pp = str(cand.resolve())
						apps_public.append(pp)
						apps_detected.append({
							"name": name,
							"path": pp,
							"type": "nuxt",
							"public": pp,
						})
						break
		except Exception:
			pass

	return apps_public, apps_detected

_PUBLIC_DIRS, APPS_DETECTED = _discover_nuxt_public_dirs()

# 3) Fallbacks runtime : accepte /app/public et /app/frontend **en plus**
def _add_runtime_public(dir_name: str, default_name: str):
	p = (BASE_DIR / dir_name).resolve()
	if (p / "index.html").exists():
		pp = str(p)
		_PUBLIC_DIRS.append(pp)
		APPS_DETECTED.append({
			"name": os.getenv("NUXT_APP_NAME", default_name),
			"path": pp,
			"type": "nuxt",
			"public": pp,
		})

_add_runtime_public("public",   "app_myFrontendNuxtVue_01")
_add_runtime_public("frontend", "app_myFrontendNuxtVue_01")

# 4) Déduplication (ne PAS vider les listes)
def _dedup_public(apps_public: list[str], apps_detected: list[dict]) -> tuple[list[str], list[dict]]:
	seen_public = set()
	public_out = []
	for p in apps_public:
		if p not in seen_public:
			seen_public.add(p)
			public_out.append(p)

	seen_detect = set()
	detected_out = []
	for app in apps_detected:
		pub = app.get("public")
		if pub and pub not in seen_detect:
			seen_detect.add(pub)
			detected_out.append(app)
	return public_out, detected_out

_PUBLIC_DIRS, APPS_DETECTED = _dedup_public(_PUBLIC_DIRS, APPS_DETECTED)

# 5) Étendre les statiques avec les builds Nuxt détectés
STATICFILES_DIRS.extend(_PUBLIC_DIRS)

# --- WhiteNoise (prod) ---
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Logs de démarrage (dev) ---
if DEBUG and os.environ.get("RUN_MAIN") == "true":
	print("\n=== Applications détectées ===")
	for app in APPS_DETECTED:
		print(f"[NUXT]  {app.get('name')}  -> {app.get('public')}")
