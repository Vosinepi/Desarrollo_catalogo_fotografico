from django import forms
from .models import Album
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from catalogo_fotos_app.models import *


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"
        exclude = []

    zip = forms.FileField(required=False)


class UserRegisterForm(UserCreationForm):
    name = forms.CharField(
        label="Nombre", max_length=30, required=False, help_text="Optional."
    )
    last_name = forms.CharField(
        label="Apellido", max_length=30, required=False, help_text="Optional."
    )
    username = forms.CharField(label="Usuario", max_length=30, required=False)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "last_name", "username", "email", "password1", "password2"]
        help_texts = {k: "" for k in fields}
