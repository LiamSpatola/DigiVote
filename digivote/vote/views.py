from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import LogInForm

# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                auth_login(request, user)
                return redirect("auth_success")
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LogInForm()
    return render(request, "login.html", {'form': form})


def logout(request):
    auth_logout(request)
    return redirect("auth_success")

def auth_success(request):
    return render(request, "auth_success.html")