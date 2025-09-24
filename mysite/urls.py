"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# mysite/mysite/urls.py
from django.contrib import admin
from django.urls import path, re_path
from django.http import FileResponse, Http404
from django.conf import settings
import os

def serve_nuxt(public_dir: str):
	def _view(request, path=''):
		index = os.path.join(public_dir, "index.html")
		if not os.path.exists(index):
			raise Http404("Nuxt index.html not found")
		return FileResponse(open(index, "rb"))
	return _view

urlpatterns = [ path("admin/", admin.site.urls) ]

for app in getattr(settings, "APPS_DETECTED", []):
	if app.get("type") == "nuxt" and app.get("public"):
		name = app["name"]
		public_dir = app["public"]
		urlpatterns.append(re_path(rf"^{name}(/.*)?$", serve_nuxt(public_dir)))