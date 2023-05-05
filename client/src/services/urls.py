from django.urls import path
from . import views

app_name = "services"
# every app will have his own conf
urlpatterns = [
    path("", views.index, name="index"),
    path("profiles/", views.services_profiles, name="profiles"),
    path("messages/", views.services_messages, name="messages"),
]
