from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("create-event/", views.create_event_post, name="create_event_post"),
]