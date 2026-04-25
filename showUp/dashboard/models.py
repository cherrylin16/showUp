from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(AbstractUser):
#     USER_TYPE_CHOICES = [
#         ('host', 'Host'),
#         ('attendee', 'Attendee'),
#         ('admin', 'Admin'),
#     ]
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

#     def is_host(self):
#         return self.user_type == 'host'
#     def is_attendee(self):
#         return self.user_type == 'attendee'
#     def __str__(self):
#         return self.username


class EventPost(models.Model):
    VISIBILITY_CHOICES = [
        ('all', 'All Users'),
    ]
    
    # author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100)
    event_name = models.TextField(default="", blank=False)
    location = models.TextField(default="",blank=False)
    caterer_address = models.TextField(default="", blank=False)
    caterer_phone = models.TextField(default="", blank=False)
    caterer_name = models.TextField(default="", blank=False)
    catering_budget = models.TextField(default="", blank=False)
    supplies_budget = models.TextField(default="", blank=False)
    date = models.TextField(default="", blank=False)
    event_description = models.TextField(default="", blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.ImageField(upload_to='carpool_posts/', blank=True, null=True)
    image_visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='all')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.username} - {self.text[:50]}"
