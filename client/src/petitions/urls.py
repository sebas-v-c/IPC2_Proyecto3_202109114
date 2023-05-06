from django.urls import path
from . import views


app_name = "petitions"

# every app will have his own conf
urlpatterns = [
    path("", views.index, name="index"),
    path("messages/", views.messages_detail, name="messages")
    # path("profiles/", views.services_profiles, name="profiles"),
    # path("messages/", views.services_messages, name="messages"),
]
