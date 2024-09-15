from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LogInForm(forms.Form):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control mb-3"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"})
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
