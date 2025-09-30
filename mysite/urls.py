# tabs = \t
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve as static_serve
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings
from django.utils.html import escapejs
import json
from pathlib import Path
import re as _re

ASSET_DIRS = ("_nuxt", "assets", "images", "icons", "fonts", "favicon.ico", "robots.txt", "sitemap.xml")

def serve_nuxt(public_dir: str):
	def _view(_req):
		index = Path(public_dir) / "index.html"
		if not index.exists():
			raise Http404("Nuxt index.html not found")
		return FileResponse(open(index, "rb"))
	return _view

def django_home(_req):
	props = {"id": 123, "size": "sm"}
	# turn props into a JSON string safe for an HTML attribute
	props_attr = escapejs(json.dumps(props))
	html = (
		f"<h1>Django OK</h1>"
		f"<p>Accueil Django sur /</p>"
		f"<div data-nuxt-component='UserCard' data-props=\"{props_attr}\"></div>"
		# In DEV, include HMR scripts; in PROD, inject built assets (see below)
	)
	return HttpResponse(html)

urlpatterns = [
	path("", django_home, name="home"),
	path("admin/", admin.site.urls),
]

# montera l'app sous /app_myFrontendNuxtVue_01/
for app in getattr(settings, "APPS_DETECTED", []):
	if app.get("type") == "nuxt" and app.get("public"):
		name = "app_myFrontendNuxtVue_01"
		public = app["public"]
		name_escaped = _re.escape(name)
		assets_alt = "|".join(_re.escape(d) for d in ASSET_DIRS)

		# 1) assets: /app_myFrontendNuxtVue_01/_nuxt/*, /assets/*, ...
		urlpatterns.append(
			re_path(
				rf"^{name_escaped}/(?P<path>(?:{assets_alt}).*)$",
				static_serve,
				{"document_root": public},
				name=f"{name}-assets",
			)
		)
		# 2) index
		urlpatterns.append(re_path(rf"^{name_escaped}/?$", serve_nuxt(public), name=f"{name}-root"))
		# 3) catch-all SPA (hors assets)
		urlpatterns.append(
			re_path(rf"^{name_escaped}/(?!(?:{assets_alt})/).+$", serve_nuxt(public), name=f"{name}-spa")
		)

