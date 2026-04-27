from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class EventPost(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='hosted_events'
    )

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='attending_events',
        blank=True
    )

    host_name = models.TextField(default="", blank=False)
    event_name = models.TextField(default="", blank=False)
    location = models.TextField(default="",blank=False)
    caterer_address = models.TextField(default="", blank=True)
    caterer_phone = models.TextField(default="", blank=True)
    caterer_name = models.TextField(default="", blank=True)
    catering_budget = models.TextField(default="", blank=True, null=True)
    supplies_budget = models.TextField(default="", blank=True, null=True)
    date = models.DateField(default="", blank=False)
    event_description = models.TextField(default="", blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
