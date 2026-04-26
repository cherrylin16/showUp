from django.db import models

class ShowUpRSVPs(models.Model):
    rsvpID = models.AutoField(primary_key=True, db_column="RSVPID")
    event = models.ForeignKey(
        'dashboard.EventPost',
        on_delete=models.CASCADE,
        db_column='eventID',
    )
    user = models.ForeignKey(
        'accounts.ShowUpUser',
        on_delete=models.CASCADE,
        db_column='userID',
    )
    status = models.CharField(max_length=10, null=False, db_column="status")
    message = models.CharField(max_length=255, db_column="message")
    
    class Meta:
        db_table = "ShowUp_RSVPs"
