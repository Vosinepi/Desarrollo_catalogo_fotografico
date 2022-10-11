#django
from email.policy import default
from django.db import models
from django.db import models
from django.contrib.auth.models import User

#libreiras de terceros
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, Transpose
import uuid
from PIL import Image

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
    es_publico = models.BooleanField(default=False)
    creada = models.DateTimeField(auto_now_add=True)
    modificada = models.DateTimeField(auto_now_add=True)
    # users_views = models.CharField( max_length=250, choices=User.objects.all().values_list('username', 'username'), default='admin')
    users_permitions = models.ManyToManyField(User, related_name="users_permitions", blank=False)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ["-creada"]

    def __unicode__(self):
        return self.titulo
    
    def __str__(self):
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    avatar = models.ImageField(default="default.jpg", upload_to="profile_images")
    bio = models.TextField(default="", blank=True)

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return self.user.username
