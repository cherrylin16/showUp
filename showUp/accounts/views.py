from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import ShowUpUser, ShowUpUserManager

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        user = ShowUpUser()

        if form.is_valid():
            user.preferenceID = 1
            user = form.save()
            login(request, user)
            print("USER CREATED:", user.email)
            return redirect("dashboard_home")
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})