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
