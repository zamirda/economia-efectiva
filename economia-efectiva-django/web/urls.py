from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("contacto/", views.contacto, name="contacto"),
    path("salud/", views.salud, name="salud"),
]
