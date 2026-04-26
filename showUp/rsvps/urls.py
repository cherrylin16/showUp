from django.urls import path

from . import views

app_name = 'rsvps'

urlpatterns = [
    path("", views.index, name="index"),
]