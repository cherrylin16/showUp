from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # return HttpResponse("RSVP Site")
    return render(request, "rsvps/index.html")