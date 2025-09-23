import os
from colorama import Fore, Style, init

init(autoreset=True)  # reset auto après chaque print

class GetNuxtApp:
    def __init__(self):
        # racine = un cran au-dessus de "mysite"
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.root_path = os.path.abspath(os.path.join(self.dir_path, ".."))
        self.apps = []  # stockage des résultats

    def scan_apps(self):
        """Scanne les dossiers app_* et les classe en Nuxt ou Django"""
        for entry in os.listdir(self.root_path):
            path = os.path.join(self.root_path, entry)
            if os.path.isdir(path) and entry.startswith("app_"):
                app_type = "nuxt" if os.path.isdir(os.path.join(path, ".nuxt")) else "django"
                self.apps.append({"name": entry, "path": path, "type": app_type})

    def display_apps(self):
        """Affiche les apps avec des couleurs"""
        print("\n=== Applications détectées ===")
        for app in self.apps:
            if app["type"] == "nuxt":
                print(Fore.GREEN + f"[NUXT]   {app['name']}  -> {app['path']}")
            elif app["type"] == "django":
                print(Fore.CYAN + f"[DJANGO] {app['name']}  -> {app['path']}")
            else:
                print(Fore.RED + f"[??]     {app['name']}  -> {app['path']}")

    def run(self):
        """Routine principale"""
        self.scan_apps()
        self.display_apps()
