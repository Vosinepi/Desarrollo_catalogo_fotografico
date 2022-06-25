from django.db import models

# Create your models here.


class Users(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class catalogo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="catalogo/")
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre
