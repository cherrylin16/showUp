from django.urls import path

from . import views

app_name = 'invites'

urlpatterns = [
    path("", views.index, name="index"),
    path("rsvp/", views.rsvp_form, name="rsvp_form")
]