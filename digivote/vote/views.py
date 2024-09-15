from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LogInForm
from .models import Choice, Poll, Vote


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                return redirect("auth_success")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LogInForm()
    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("auth_success")


def auth_success(request):
    return render(request, "auth_success.html")


@login_required(login_url="login")
def polls(request):
    polls = Poll.objects.all()
    context = {"polls": polls}
    return render(request, "polls.html", context)


@login_required(login_url="login")
def details(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll)
    poll.update_status()
    total_votes = sum(choice.votes for choice in choices)
    highest_vote = max(choice.votes for choice in choices)

    if total_votes <= 0:
        winners = []
    else:
        winners = [choice for choice in choices if choice.votes == highest_vote]

    choices_with_percentage = []
    for choice in choices:
        if total_votes > 0:
            vote_percentage = round((choice.votes / total_votes) * 100, 2)
        else:
            vote_percentage = 0
        
        choices_with_percentage.append(
        {"choice": choice, "percentage": vote_percentage}
        )

    now = timezone.now()
    time_remaining = poll.close_date - now
    days, seconds = time_remaining.days, time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds."

    context = {
        "poll": poll,
        "choices": choices_with_percentage,
        "winners": winners,
        "total_votes": total_votes,
        "time_remaining": time_remaining_str
    }
    return render(request, "details.html", context)


@login_required(login_url="login")
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.update_status()
    choices = Choice.objects.filter(poll=poll)
    context = {"poll": poll, "choices": choices}
    return render(request, "vote.html", context)


@login_required(login_url="login")
def record_vote(request, poll_id, choice_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.update_status()
    choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
    user_has_voted = Vote.objects.filter(user=request.user, poll=poll).exists()
    if user_has_voted or not poll.poll_open:
        return redirect("vote_fail")
    else:
        Vote.objects.create(user=request.user, choice=choice, poll=poll)
        choice.votes += 1
        choice.save()
        return redirect("vote_success")


@login_required(login_url="login")
def vote_fail(request):
    return render(request, "vote_fail.html")


@login_required(login_url="login")
def vote_success(request):
    return render(request, "vote_success.html")


@login_required(login_url="login")
def my_votes(request):
    votes = Vote.objects.filter(user=request.user)
    context = {"votes": votes}
    return render(request, "my_votes.html", context)