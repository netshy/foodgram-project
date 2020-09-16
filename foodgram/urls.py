"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.views.generic import RedirectView

from foodgram import settings
from django.contrib import admin
from django.urls import path, include
# noinspection PyRedeclaration
from django.conf.urls import handler404, url

# noinspection PyRedeclaration
handler404 = "recipes.views.page_not_found"

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/images/favicon.ico', permanent=True)),
    path('admin/panel/', admin.site.urls, name='admin-panel'),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
