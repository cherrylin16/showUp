from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("Setting up our initial Django app.")
    return render(request, "dashboard/home.html")

