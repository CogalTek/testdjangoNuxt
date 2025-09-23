from pathlib import Path
import os

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
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],  # optionnel mais pratique
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
STATIC_ROOT = BASE_DIR / 'staticfiles'      # utile en prod (collectstatic)
STATICFILES_DIRS: list[str | os.PathLike] = [BASE_DIR / 'static']  # répertoire statique "app" (optionnel)

# Découverte auto des builds Nuxt (.output/public) dans tous les app_* à la racine du repo ou sous ./mysite
def _discover_nuxt_public_dirs() -> tuple[list[str], list[dict]]:
	apps_public = []
	apps_detected = []

	# on cherche à la racine du repo (parent de BASE_DIR) ET dans BASE_DIR (si des app_* sont là)
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

			# Critères "Nuxt" : présence d'un dossier .nuxt (ta contrainte) ET d'un build disponible
			nuxt_marker = os.path.isdir(os.path.join(app_dir, ".nuxt"))
			public_dir = os.path.join(app_dir, ".output", "public")
			is_public = os.path.isdir(public_dir)

			app_type = "nuxt" if nuxt_marker else "django"
			apps_detected.append({
				"name": entry,
				"path": app_dir,
				"type": app_type,
				"public": public_dir if is_public else None,
				"nuxt_marker": nuxt_marker,
			})

			# On n'ajoute aux statiques que si le build Nuxt existe réellement
			if app_type == "nuxt" and is_public:
				apps_public.append(public_dir)

	return apps_public, apps_detected

_PUBLIC_DIRS, APPS_DETECTED = _discover_nuxt_public_dirs()
STATICFILES_DIRS.extend(_PUBLIC_DIRS)

# APPS_DETECTED est maintenant accessible partout:
# from django.conf import settings; settings.APPS_DETECTED
