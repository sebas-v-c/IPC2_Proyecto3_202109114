from django.shortcuts import render

# Create your views here.


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
    return render(
        request,
        "help/index.html",
        {"current": request.path.strip("/").split()[0]},
    )
