from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            print("USER CREATED:", user.email)
            return redirect("dashboard_home")
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})