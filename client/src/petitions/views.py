from django.core import files
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

import requests

# Create your views here.


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

        if all:
            response = requests.post(
                settings.API_URL + "/messages/detail/all/",
                json={"date": date},
                headers={"Content-Type": "application/json"},
            )

            pdf_content = response.content
            context["pdf_content"] = pdf_content

            return render(request, "petitions/search.html", context)

        return render(request, "petitions/search.html", context)
        # if all:
        #     response = requests.post(
        #         settings.API_URL + "/messages/detail/all/",
        #     )

        # form = XmlForm(request.POST, request.FILES)
        # if form.is_valid():
        #     xml_file = request.FILES["xml_file"]
        #     if xml_file.name.endswith(".xml"):
        #         response = requests.post(
        #             settings.API_URL + "/users/profiles", files={"file": xml_file}
        #         )
        #         if response.status_code == 200:
        #             xml_response = response.content.decode("utf-8")
        #             context["res"] = xml_response
        #             return render(request, "services/load.html", context)
    elif request.method == "GET":
        return render(request, "petitions/search.html", context)

    # if everything fail
    context["res"] = "Hubo un error con la API"
    return render(request, "petitions/search.html", context)
