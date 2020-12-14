"""farmify URL Configuration

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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views as v

urlpatterns = [
    # other app urls
    path('admin/', admin.site.urls),
    path('auth/',include('auths.urls')),
    path('farmers/',include('farmers.urls')),
    path('dealers/',include('dealers.urls')),
    path('news/',include('news.urls')),
    path('apiexpo/',include('apiexpo.urls')),
    
    # this app urls
    path('',v.landing_view,name="landing_page"),
    path('contact',v.contact,name="contact"),
    path('search',v.search,name="search"),
    path('weather',v.weather,name="weather")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
