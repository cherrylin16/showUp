from django.contrib.auth.forms import UserCreationForm
from .models import ShowUpUser
from django import forms

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
            "password1",
            "password2",
        )

        widgets = {
            "firstName": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name",
            }),
            "lastName": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "name@example.com",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "123-456-7890",
            }),
            "birthdate": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "pfp": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional fields
        self.fields["phone"].required = False
        self.fields["birthdate"].required = False
        self.fields["pfp"].required = False

        # Bootstrap password fields
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password",
        })

        self.fields["birthdate"].help_text = "Optional. Use the date picker or YYYY-MM-DD."
        # self.fields["password1"].help_text = "Your password must meet the rules listed below."
        
        
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