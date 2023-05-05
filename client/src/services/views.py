from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def services_page(request):
    return render(
        request,
        "services/index.html",
        {"doc": "Document Here", "current": request.path.strip("/").split()[0]},
    )


def services_profiles(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "load.html")
