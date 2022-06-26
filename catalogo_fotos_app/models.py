from django.db import models
import uuid
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose

# Create your models here.


class Users(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


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
    album = models.ForeignKey("album", on_delete=models.PROTECT)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    creada = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)