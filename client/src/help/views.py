from django.http import FileResponse
from django.shortcuts import render
from django.conf import settings
import requests
import os
import tempfile

# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(
        request,
        "help/index.html",
        {"current": request.path.strip("/").split()[0]},
    )


def about(request):
    return render(
        request,
        "help/about.html",
        {"current": request.path.strip("/").split()[0]},
    )


def documentation(request):
    temp_dir = tempfile.TemporaryDirectory(dir=BASE_DIR)
    temp_path = temp_dir.name
    file_path = os.path.join(temp_path, "output.pdf")

    response = requests.get(
        settings.API_URL + f"/doc/",
    )

    with open(file_path, "wb") as f:
        f.write(response.content)

    print(file_path)
    return FileResponse(
        open(file_path, "rb"),
        filename="ensayo.pdf",
        content_type="application/pdf",
    )
