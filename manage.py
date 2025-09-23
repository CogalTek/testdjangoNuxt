import os
import sys
from script.getNuxtApp import GetNuxtApp

def main():
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
	try:
		from django.core.management import execute_from_command_line
	except ImportError as exc:
		raise ImportError(
			"Couldn't import Django. Are you sure it's installed and "
			"available on your PYTHONPATH environment variable? Did you "
			"forget to activate a virtual environment?"
		) from exc

	# ta routine de démarrage
	LISTAPP = GetNuxtApp()
	LISTAPP.run()

	execute_from_command_line(sys.argv)

if __name__ == "__main__":
	main()
