from django.core import files
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

from .forms import XmlForm
import requests

# Create your views here.


def index(request):
    return render(
        request,
        "services/index.html",
        {"current": request.path.strip("/").split()[0]},
    )


def services_profiles(request):
    context = {
        "page_title": "Carga de Perfiles",
        "upload_url": reverse("services:profiles"),
    }
    if request.method == "POST":
        form = XmlForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES["xml_file"]
            if xml_file.name.endswith(".xml"):
                response = requests.post(
                    settings.API_URL + "/users/profiles", files={"file": xml_file}
                )
                if response.status_code == 200:
                    xml_response = response.content.decode("utf-8")
                    context["res"] = xml_response
                    return render(request, "services/load.html", context)
    elif request.method == "GET":
        return render(request, "services/load.html", context)

    # if everything fail
    context["res"] = "Hubo un error con la API"
    return render(request, "services/load.html", context)


def services_messages(request):
    context = {
        "page_title": "Carga de Mensajes",
        "upload_url": reverse("services:messages"),
    }
    if request.method == "POST":
        xml_file = request.FILES["xml_file"]
        if xml_file.name.endswith(".xml"):
            response = requests.post(
                settings.API_URL + "/messages/new", files={"file": xml_file}
            )
            if response.status_code == 200:
                xml_response = response.content.decode("utf-8")
                context["res"] = xml_response
                return render(request, "services/load.html", context)
    else:
        context = {"page_title": "Carga de Mensajes"}
        return render(request, "services/load.html", context)

    context["res"] = "Hubo un error con la API"
    return render(request, "services/load.html", context)
