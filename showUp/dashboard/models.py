from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



from django.db import models
from django.conf import settings

class EventPost(models.Model):
    id = models.AutoField(primary_key=True, db_column='eventID')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        db_column='hostID',
        related_name='hosted_events'
    )

    event_name = models.TextField(db_column='eventName')
    event_description = models.TextField(db_column='description', blank=True)

    date = models.DateField(db_column='date')
    
    time = models.TimeField(db_column='time') 
    
    location = models.TextField(db_column="location")

    class Meta:
        managed = False  
        db_table = 'ShowUp_Events'

class Budget(models.Model):
    budgetID = models.AutoField(primary_key=True)
    event = models.ForeignKey(EventPost, on_delete=models.CASCADE, db_column='eventID')
    catering = models.DecimalField(max_digits=10, decimal_places=2, db_column='catering')
    party_supplies = models.DecimalField(max_digits=10, decimal_places=2, db_column='partySupplies')

    class Meta:
        managed = False
        db_table = 'ShowUp_Budgets'


class Caterer(models.Model):
    name = models.CharField(primary_key=True, db_column='catererName', max_length=255)
    phone = models.CharField(max_length=20, db_column='phoneNumber')
    location = models.TextField(db_column='location')

    class Meta:
        managed = False
        db_table = 'Caterers'


class Catering(models.Model):
    cateringID = models.AutoField(primary_key=True)
    event = models.ForeignKey('EventPost', on_delete=models.CASCADE, db_column='eventID', related_name='catering_info')
    caterer = models.ForeignKey(Caterer, on_delete=models.CASCADE, db_column='catererName')
    special_instructions = models.TextField(db_column='specialInstruction')

    class Meta:
        managed = False
        db_table = 'Catering'
    

class EventPhoto(models.Model):
    event = models.ForeignKey(
        EventPost,
        on_delete=models.CASCADE,
        related_name="photos",
        db_column="event_id",
    )

    image = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ShowUp_EventPhotos"
