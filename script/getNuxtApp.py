# tabs = \t
import os
from colorama import Fore, init
from django.conf import settings
from pathlib import Path

init(autoreset=True)

def print_mounted_apps():
	print("\n=== Applications détectées ===")
	# 1) depuis settings.APPS_DETECTED (ce que Django utilise réellement)
	for app in getattr(settings, "APPS_DETECTED", []):
		typ = app.get("type")
		name = app.get("name")
		path = app.get("public") or app.get("path")
		if typ == "nuxt":
			print(Fore.GREEN + f"[NUXT]   {name}  -> {path}")
		elif typ == "django":
			print(Fore.CYAN + f"[DJANGO] {name}  -> {path}")
		else:
			print(Fore.YELLOW + f"[AUTO]   {name}  -> {path}")

	# 2) fallback: si /app/frontend existe mais n’a pas été ajouté (sécurité)
	frontend = (settings.BASE_DIR / "frontend")
	if frontend.exists() and all((app.get("public") != str(frontend)) for app in getattr(settings, "APPS_DETECTED", [])):
		print(Fore.GREEN + f"[NUXT]   (fallback)  -> {frontend}")
