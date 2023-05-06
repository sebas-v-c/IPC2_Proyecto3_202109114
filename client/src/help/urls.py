from django.urls import path
from . import views


app_name = "help"

# every app will have his own conf
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("documentation/", views.documentation, name="documentation"),
]
