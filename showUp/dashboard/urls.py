from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("create-event/", views.create_event_post, name="create_event_post"),
    path("events/<int:post_id>/photos/upload/", views.upload_event_photo, name="upload_event_photo"),
    path("photos/<int:photo_id>/delete/", views.delete_event_photo, name="delete_event_photo"),
     path("events/<int:post_id>/invite_guest/", views.invite_guest, name="invite_guest"),
]