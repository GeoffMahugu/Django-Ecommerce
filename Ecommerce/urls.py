"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    login,
    logout
)
from django.contrib.auth import views as auth_views
from Products.urls import Home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/', Home ),
    url(r'^', Home ),
    url(r'^Products/', include("Products.urls", namespace='Products' )),
    url(r'^Cart/', include("Cart.urls", namespace='Cart' )),
]
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
