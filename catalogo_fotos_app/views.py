from msilib.schema import ListView
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, DeleteView, FormView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import *
from .models import Album, AlbumImage
from .admin import *


def quien_soy(request):
    return render(request, "quien_soy.html")


def index(request):

    return render(
        request,
        "index.html",
    )


# catalogo


def catalogo(request):
    list = Album.objects.filter(is_visible=True).order_by("-creada")
    paginator = Paginator(list, 10)

    page = request.GET.get("page")
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(
            paginator.num_pages
        )  # If page is out of range (e.g.  9999), deliver last page of results.
    return render(request, "catalogo.html", {"albums": list})


# vista detallada de un album
class AlbumDetail(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        print(context)
        # Add in a QuerySet of all the images
        context["images"] = AlbumImage.objects.filter(album=self.object.id)
        print(len(context["images"]))
        if len(context["images"]) == 0:
            return None
        else:
            print(context["images"][0].album.slug)
            return context


# carga de albumes por app
class CargarAlbum(LoginRequiredMixin, FormView):
    model = Album
    template_name = "cargar_album.html"
    form_class = AlbumForm
    prepopulated_fields = {"slug": ("titulo",)}
    success_url = "exito"
    print("cargar album")

    def form_valid(self, form):
        print("funcion save_model")
        print("validacion ok")
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
                img.tags = album.tags
                img.album_titulo = album.titulo
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
        return super(CargarAlbum, self).form_valid(form)


def subida_exitosa(request):
    return render(request, "subida_exitosa.html")


# inicio de sesion
# def user_login(request, auth_form=LoginForm):

#     if request.method == "POST":
#         print("post valido")
#         form = auth_form(request.POST)
#         if form.is_valid():
#             print("valido")
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")

#             if not form.cleaned_data.get("remember_me"):
#                 request.session.set_expiry(0)
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # cierra la sesión
#                 return redirect("index")
#             else:
#                 return render(request, "login.html", {"form": form})
#         else:
#             print("auth no valido")
#             return render(request, "login.html", {"form": form})
#     form = LoginForm()
#     return render(request, "login.html", {"form": form})


class User_Login(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    print("login")

    class User_Login(LoginView):
        form_class = LoginForm

        def form_valid(self, form):

            remember_me = form.cleaned_data[
                "remember_me"
            ]  # get remember me data from cleaned_data of form
            if not remember_me:
                print("expira cuando se cierre navegador")
                self.request.session.set_expiry(0)  # if remember me is
                self.request.session.modified = True
            return super(User_Login, self).form_valid(form)


def logOut(request):
    logout(request)
    return redirect("user_login")


# registro usuarios
def register_user(request):
    """
    Si el método de solicitud es POST, valide el formulario, si el formulario es válido, guarde el
    formulario, si el formulario no es válido, imprima "no valido" y devuelva el formulario

    :param request: El objeto de solicitud es un objeto Django que contiene metadatos sobre la solicitud
    actual
    :return: El formulario está siendo devuelto.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            print(username)
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Cuenta creada para " + user)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return redirect("login")
        else:
            print("no valido")
            messages.error(request, "Error al procesar solicitud")

        print("no valido")
        return render(request, "accounts/registro_usuario.html", {"form": form})
    form = UserRegisterForm()

    return render(request, "accounts/registro_usuario.html", {"form": form})


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            user = User.objects.filter(Q(email=data))
            if user.exists():
                for user in user:
                    subject = "Recuperar contraseña"
                    email_template = "accounts/mail_text.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Fotos PRO",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template, c)
                    recipient_list = [settings.EMAIL_HOST_USER]
                    try:
                        send_mail(
                            subject,
                            email,
                            user.email,
                            recipient_list,
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    messages.success(
                        request,
                        "Un mensaje con las instrucciones para el reseteo de su contraseña fue enviado a su casilla de correo.",
                    )
                    return redirect("index")
            messages.error(request, "No existe un usuario con ese correo electrónico.")

    form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {"form": form})


class Cambiar_password(PasswordChangeView):
    template_name = "accounts/cambiar_password.html"
    success_message = "Contraseña cambiada correctamente"
    success_url = reverse_lazy("index")


@login_required
def perfil(request):
    user_form = ActualizarUserForm(instance=request.user)
    perfil_form = ActualizarPerfilForm(instance=request.user.profile)
    if request.method == "POST":
        user_form = ActualizarUserForm(request.POST, instance=request.user)
        perfil_form = ActualizarPerfilForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect("user")
        else:
            user_form = ActualizarUserForm(instance=request.user)
            perfil_form = ActualizarPerfilForm(instance=request.user.profile)

    return render(
        request,
        "accounts/user.html",
        {"user_form": user_form, "perfil_form": perfil_form},
    )


# eliminar fotos desde vita detalle
@user
def eliminar_foto(request, id):
    foto = AlbumImage.objects.get(id=id)
    foto.delete()

    return redirect("album", slug=foto.album.slug)


# vista base
def base(request):
    return render(request, "template_base.html")


def terminos_condiciones(request):  # vista de terminos y condiciones
    return render(request, "terminos_y_condiciones.html")


# buscador
def busqueda(request):
    """
    Retorna una lista de fotos que coincidan con el criterio de busqueda.
    Tambien retorna los albumes a los que pertenecen las fotos y el slug para
    generar los enlaces a los mismos.
    """

    buscar_foto = request.GET.get("busqueda")
    album = Album.objects.all()

    if buscar_foto:
        print("buscar foto")
        fotos = AlbumImage.objects.filter(
            Q(alt__icontains=buscar_foto) | Q(tags__icontains=buscar_foto)
        )

    else:
        fotos = AlbumImage.objects.all()
    titulos_albumes = []
    slug_albumes = []

    for foto in fotos:

        titulos_albumes.append(
            foto.album_titulo
        ) if foto.album_titulo not in titulos_albumes else titulos_albumes
    for titulo in album:
        slug_albumes.append(
            titulo.slug
        ) if titulo.slug not in slug_albumes else slug_albumes
    titulos_albumes.sort()
    slug_albumes.sort()
    res = dict(zip(titulos_albumes, slug_albumes))
    print(res)

    return render(request, "buscador.html", {"fotos": fotos, "titulos_albumes": res})


def contacto(request):
    form = Contactos()

    if request.method == "POST":
        form = Contactos(request.POST)
        if form.is_valid():
            print("form validado")
            nombre = form.cleaned_data.get("nombre")
            apellido = form.cleaned_data.get("apellido")
            email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            menssage = form.cleaned_data.get("message")

            form.save()
            recipient_list = [settings.EMAIL_HOST_USER]
            mensaje = f"Nombre: {nombre}\n Apellido: {apellido}\nEmail: {email}\nAsunto: {subject}\nMensaje: {menssage}"

            send_mail(subject, mensaje, email, recipient_list)

            return render(request, "gracias.html")
    else:
        form = Contactos()

    return render(request, "contacto.html", {"form": form})


# def carrito(request):
#     return render(request, "carrito.html")
