from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Preference, ShowUpUser
from .forms import SignUpForm, ProfileUpdateForm, PreferenceUpdateForm
from django.contrib.auth.decorators import login_required
from .models import ShowUpUser, ShowUpUserManager

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        user = ShowUpUser()

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
        profile_form = ProfileUpdateForm(request.POST, instance=user)
        preference_form = PreferenceUpdateForm(request.POST, instance=user.preference)

        if profile_form.is_valid() and preference_form.is_valid():
            ShowUpUser.objects.filter(userID=user.userID).update(
                firstName=profile_form.cleaned_data["firstName"],
                lastName=profile_form.cleaned_data["lastName"],
                email=profile_form.cleaned_data["email"],
                phone=profile_form.cleaned_data["phone"],
                birthdate=profile_form.cleaned_data["birthdate"],
            )

            preference_form.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        profile_form = ProfileUpdateForm(instance=user)
        preference_form = PreferenceUpdateForm(instance=user.preference)

    return render(request, "accounts/profile.html", {
        "form": profile_form,
        "preference_form": preference_form,
    })