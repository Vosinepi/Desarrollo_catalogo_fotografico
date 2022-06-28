from django import forms
from .models import Album


from catalogo_fotos_app.models import *


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"
        exclude = []

    zip = forms.FileField(required=False)
