from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, DeleteView, FormView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import *
from .models import Album, AlbumImage
from .admin import *


def index(request):
    return render(request, "index.html")


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

        # Add in a QuerySet of all the images
        context["images"] = AlbumImage.objects.filter(album=self.object.id)
        print(context["images"][0].album.slug)
        return context


# carga de albumes por app
class CargarAlbum(LoginRequiredMixin, FormView):
    model = Album
    template_name = "cargar_album.html"
    form_class = AlbumForm
    success_url = "exito"

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
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return render(request, "login.html", {"form": form})
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logOut(request):
    logout(request)
    return redirect("index")


def register_user(request):
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
        return render(request, "registro_usuario.html", {"form": form})
    form = UserRegisterForm()
    return render(request, "registro_usuario.html", {"form": form})


# vista base
def base(request):
    return render(request, "template_base.html")


class Registro_usuario(TemplateView):
    template_name = "registro_usuario.html"


def terminos_condiciones(request):
    return render(request, "terminos_y_condiciones.html")
