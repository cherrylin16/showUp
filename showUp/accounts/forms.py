from django.contrib.auth.forms import UserCreationForm
from .models import ShowUpUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = ShowUpUser
        fields = (
            "firstName",
            "lastName",
            "email",
            "phone",
            "birthdate",
            "pfp",
            "preferenceID",
            "password1",
            "password2",
        )
        
        
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))