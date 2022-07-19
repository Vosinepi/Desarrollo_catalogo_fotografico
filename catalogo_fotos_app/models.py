from django.db import models
import uuid
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose

# Create your models here.


class Album(models.Model):
    titulo = models.CharField(max_length=70)
    descripcion = models.TextField(max_length=1024)
    thumb = ProcessedImageField(
        upload_to="albums",
        processors=[Transpose(), ResizeToFit(300)],
        format="JPEG",
        options={"quality": 90},
    )
    tags = models.CharField(max_length=250)
    is_visible = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now_add=True)
    modificada = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["-creada"]

    def __unicode__(self):
        return self.titulo


class AlbumImage(models.Model):
    image = ProcessedImageField(
        upload_to="albums",
        processors=[Transpose(), ResizeToFit(1280)],
        format="JPEG",
        options={"quality": 70},
    )
    thumb = ProcessedImageField(
        upload_to="albums",
        processors=[Transpose(), ResizeToFit(300)],
        format="JPEG",
        options={"quality": 80},
    )
    album = models.ForeignKey("album", on_delete=models.CASCADE)
    album_titulo = models.CharField(max_length=250)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    tags = models.CharField(max_length=250)
    creada = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)

    # def __str__(self):
    #     return self.alt


# class Carrito(models.Model):
#     usuario = models.ForeignKey("auth.User", on_delete=models.CASCADE)
#     producto = models.ForeignKey("AlbumImage", on_delete=models.CASCADE)
#     cantidad = models.IntegerField(default=1)
#     creada = models.DateTimeField(auto_now_add=True)
#     modificada = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)


class Contacto(models.Model):
    nombre = models.CharField(max_length=70)
    apellido = models.CharField(max_length=70)
    email = models.EmailField()
    subject = models.CharField(max_length=70)
    menssage = models.TextField(max_length=1024)
    creada = models.DateTimeField(auto_now_add=True)
    modificada = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.nombre
