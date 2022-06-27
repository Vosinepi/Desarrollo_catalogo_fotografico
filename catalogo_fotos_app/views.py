from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Album, AlbumImage
from .admin import *


def index(request):
    return render(request, "index.html")


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


class AlbumDetail(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context["images"] = AlbumImage.objects.filter(album=self.object.id)
        return context


@login_required
def cargar_album(request):

    if request.method == "POST":
        form = CargarAlbum(request.POST, request.FILES)
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

    else:
        form = CargarAlbum()

    return render(
        request,
        "cargar_album.html",
        {"carga_familia_form": CargarAlbum},
    )


def user_login(request):
    if request.method == "POST":
        # Process the request if posted data are available
        username = request.POST["username"]
        password = request.POST["password"]
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, "index.html")
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(
                request,
                "login.html",
                {"error_message": "Incorrect username and / or password."},
            )
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, "login.html")


def base(request):
    return render(request, "template_base.html")
