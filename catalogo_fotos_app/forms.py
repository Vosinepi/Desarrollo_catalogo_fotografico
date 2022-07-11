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
        # widgets = {
        #     "slug": forms.HiddenInput()
        # }  # para que no se muestre en el formulario pero tampoco se muestra en admin. VER ESTO

    zip = forms.FileField(required=False)


class UserRegisterForm(UserCreationForm):
    name = forms.CharField(
        label="Nombre",
        max_length=30,
        required=False,
        help_text="Ingresa tu nombre",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Ingresa tu apellido",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    username = forms.CharField(
        label="Usuario",
        max_length=30,
        required=True,
        help_text="Ingresa tu usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        help_text="Ingresa tu email",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        help_text="Ingresa tu contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label="Repetir contraseña",
        required=True,
        help_text="Repite tu contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    # check = forms.BooleanField(
    #     required=True,
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "type": "checkbox",
    #         }
    #     ),
    # )

    class Meta:
        model = User
        fields = [
            "name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]
        help_texts = {k: "" for k in fields}
