from django import forms
from .models import Album
import os
import uuid
import zipfile
import proyecto_final_coder.settings
from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.base import ContentFile

from PIL import Image


from catalogo_fotos_app.models import *


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)


class CargarAlbum(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)

    prepopulated_fields = {"slug": ("titulo",)}
    list_display = ("titulo", "thumb")
    list_filter = ("creada",)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()

            if form.cleaned_data["zip"] != None:
                zip = zipfile.ZipFile(form.cleaned_data["zip"])
                for filename in sorted(zip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename
                    filename = "{0}{1}.jpg".format(album.slug, str(uuid.uuid4())[-13:])
                    img.image.save(filename, contentfile)

                    filepath = "{0}/albums/{1}".format(
                        proyecto_final_coder.settings.MEDIA_ROOT, filename
                    )
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save("thumb-{0}".format(filename), contentfile)
                    img.save()
                zip.close()
            super(CargarAlbum, self).save_model(request, obj, form, change)
