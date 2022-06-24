from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("catalogo/", catalogo, name="catalogo"),
    path("login/", log_in, name="login"),
]
