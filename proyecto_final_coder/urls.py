"""proyecto_final_coder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

import catalogo_fotos_app.views as views

app_name = (
    "mymodule"  # app name para logeo: {% url 'mymodule:user_login' %} en template.
)
urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("base/", views.base, name="base"),
    path("", views.index, name="index"),
    path("cargar_album/exito/", views.subida_exitosa, name="subida_exitosa"),
    re_path(r"catalogo", views.catalogo, name="catalogo"),  # albumes
    re_path(r"^album/(?P<slug>[-\w]+)$", views.AlbumDetail.as_view(), name="album"),
    path("cargar_album/", views.CargarAlbum.as_view(), name="cargar_album"),
    path("registro_usuario/", views.register_user, name="registro_usuario"),
    path("eliminar-foto/<int:id>/", views.eliminar_foto, name="eliminar_foto"),
    re_path("buscador/", views.busqueda, name="buscador"),
    re_path("contacto/", views.contacto, name="contacto"),
    re_path(
        "login/",
        views.User_Login.as_view(),
        name="user_login",
    ),
    path("logout/", views.logOut, name="user_logout"),
    path("perfil/", views.perfil, name="user"),
    path("terminos.html", views.terminos_condiciones, name="terminos"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("password_reset/", views.password_reset, name="password_reset"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
