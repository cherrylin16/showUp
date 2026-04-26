from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Preference, ShowUpUser
from .forms import SignUpForm, ProfileUpdateForm, PreferenceUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            pref = Preference.objects.create(
                lightMode="Light",
                notifications=True
            )

            user = form.save(commit=False)
            user.preference = pref
            user.save()

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
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)

        if form.is_valid():
            ShowUpUser.objects.filter(userID=user.userID).update(
                firstName=form.cleaned_data["firstName"],
                lastName=form.cleaned_data["lastName"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                birthdate=form.cleaned_data["birthdate"],
            )

            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            print(form.errors)
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "accounts/profile.html", {"form": form})