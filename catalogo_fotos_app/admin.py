from django.contrib import admin

from catalogo_fotos_app.models import *


# Register your models here.


class Users(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "mail", "user", "password")
    search_fields = ("nombre", "apellido", "mail", "user")


class Catalogo(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "imagen", "precio")
    search_fields = ("nombre", "descripcion", "imagen", "precio")


admin.site.register(Catalogo, Catalogo)
admin.site.register(Users, Users)
