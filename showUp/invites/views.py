from django.shortcuts import render
from django.http import HttpResponse
from .models import ShowUpRSVPs
from django.db import connection

def index(request):
    invites = None
    if request.user.is_authenticated:
        userID = request.user.userID
        invites = ShowUpRSVPs.objects.filter(user=userID)
    context = {"user_invites" : invites}
    return render(request, "invites/index.html", context)

def rsvp_form(request):
    return render(request, "invites/rsvp_form.html")
