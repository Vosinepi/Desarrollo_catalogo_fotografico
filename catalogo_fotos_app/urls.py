from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path("catalogo/", catalogo, name="catalogo"),
    path("cargar_album/", cargar_album, name="cargar_album"),
    path("login/", log_in, name="login"),
]
