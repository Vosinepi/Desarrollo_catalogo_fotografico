from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView

from .models import Album, AlbumImage


def index(request):
    return render(request, "index.html")


def template_base(request):
    return render(request, "template_base.html")


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


def cargar_album(request):
    return render(request, "cargar_album.html")


def log_in(request):
    return render(request, "login.html")


def base(request):
    return render(request, "template_base.html")
