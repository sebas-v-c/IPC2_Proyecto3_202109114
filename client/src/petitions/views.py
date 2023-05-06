from django.core import files
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.urls import reverse
from base64 import b64encode

from .forms import XmlForm

import os
import tempfile

import requests

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request, "petitions/index.html")


def messages_detail(request):
    context = {
        "page_title": "Detalle de mensajes",
        "show_date": True,
        "post_url": reverse("petitions:messages"),
    }
    if request.method == "POST":
        date = request.POST.get("date_field").split("-")
        all = request.POST.get("all_input")
        username = request.POST.get("username")

        if date[0]:
            date[0], date[2] = date[2], date[0]
            date = "/".join(date)
        else:
            date = ""
        temp_dir = tempfile.TemporaryDirectory(dir=BASE_DIR)
        temp_path = temp_dir.name
        file_path = os.path.join(temp_path, "output.pdf")

        response = None

        if all:
            response = requests.get(
                settings.API_URL + "/messages/detail/all/",
                json={"date": date},
                headers={"Content-Type": "application/json"},
            )
            # pdf_content = b64encode(response.content).decode("utf-8")
            # context["pdf_content"] = pdf_content
        elif username:
            response = requests.get(
                settings.API_URL + f"/messages/detail/{username}",
                json={"date": date},
                headers={"Content-Type": "application/json"},
            )
        else:
            context["error"] = True
            return render(request, "petitions/search.html", context)

        if response.status_code == 404:
            context["no_file"] = True
            return render(request, "petitions/search.html", context)

        with open(file_path, "wb") as f:
            f.write(response.content)

        return FileResponse(
            open(file_path, "rb"),
            filename="output.pdf",
            content_type="application/pdf",
        )
    elif request.method == "GET":
        return render(request, "petitions/search.html", context)


def user_weight(request):
    context = {
        "page_title": "Resumenes de Peso",
        "show_date": False,
        "post_url": reverse("petitions:weights"),
    }
    if request.method == "POST":
        all = request.POST.get("all_input")
        username = request.POST.get("username")

        temp_dir = tempfile.TemporaryDirectory(dir=BASE_DIR)
        temp_path = temp_dir.name
        file_path = os.path.join(temp_path, "output.pdf")

        response = None

        if all:
            response = requests.get(
                settings.API_URL + "/users/weights/all/",
            )
            # pdf_content = b64encode(response.content).decode("utf-8")
            # context["pdf_content"] = pdf_content
        elif username:
            response = requests.get(
                settings.API_URL + f"/users/weights/{username}",
            )
        else:
            context["error"] = True
            return render(request, "petitions/search.html", context)

        if not response.content:
            context["no_file"] = True
            return render(request, "petitions/search.html", context)

        with open(file_path, "wb") as f:
            f.write(response.content)

        return FileResponse(
            open(file_path, "rb"),
            filename="output.pdf",
            content_type="application/pdf",
        )
    elif request.method == "GET":
        return render(request, "petitions/search.html", context)


def tests(request):
    context = {
        "page_title": "Prueba de Mensaje",
        "upload_url": reverse("petitions:tests"),
    }
    if request.method == "POST":
        form = XmlForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES["xml_file"]
            if xml_file.name.endswith(".xml"):
                response = requests.post(
                    settings.API_URL + "/test", files={"file": xml_file}
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
