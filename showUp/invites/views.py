from django.shortcuts import render
from django.http import HttpResponse
from .models import ShowUpRSVPs


def index(request):
    invites = None
    if request.user.is_authenticated:
        user = request.user.id
        invites = ShowUpRSVPs.objects.filter(userid=user)
    context = {"user_invites" : invites}
    return render(request, "invites/index.html", context)

def rsvp_form(request):
    return render(request, "invites/rsvp_form.html")
