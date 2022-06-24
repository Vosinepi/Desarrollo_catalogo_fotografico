from django.shortcuts import render, redirect


def index(request):

    return render(request, "index.html")


def template_base(request):
    return render(request, "template_base.html")


def catalogo(request):
    return render(request, "catalogo.html")


def log_in(request):
    return render(request, "login.html")
