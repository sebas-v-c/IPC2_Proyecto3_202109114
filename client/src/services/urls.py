from django.urls import path
from . import views

# every app will have his own conf
urlpatterns = [
    path("", views.services_page, name="services"),
    path("profiles/", views.services_profiles, name="profiles"),
    path("messages", views.services_profiles, name="messages"),
]
