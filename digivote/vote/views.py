import json
import os

import pyrankvote
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from dotenv import load_dotenv
from pyrankvote import Ballot as PyRankBallot
from pyrankvote import Candidate as PyRankCandidate

from .forms import ElectionVote, LogInForm, RegisterForm
from .models import Ballot, Candidate, Choice, Election, Poll, Vote

load_dotenv()


def update_polls():
    # Internal use only. Not a view
    polls = Poll.objects.all()
    for poll in polls:
        poll.update_status()


def update_elections():
    # Internal use only. Not a view
    elections = Election.objects.all()
    for election in elections:
        election.update_status()


def index(request):
    update_polls()
    update_elections()
    return render(request, "index.html")


def login(request):
    update_polls()
    update_elections()
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
    update_polls()
    update_elections()
    auth_logout(request)
    return redirect("auth_success")


def auth_success(request):
    update_polls()
    update_elections()
    return render(request, "auth_success.html")


@login_required(login_url="login")
def polls(request):
    update_polls()
    update_elections()

    polls = Poll.objects.all()
    context = {"polls": polls}
    return render(request, "polls.html", context)


@login_required(login_url="login")
def details(request, poll_id):
    update_polls()
    update_elections()

    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll)
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
    time_remaining_str = (
        f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    )

    time_until_open = now - poll.open_date
    days, seconds = time_until_open.days, time_until_open.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_until_open_str = (
        f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    )

    context = {
        "poll": poll,
        "choices": choices_with_percentage,
        "winners": winners,
        "total_votes": total_votes,
        "time_remaining": time_remaining_str,
        "time_until_open": time_until_open_str,
    }
    return render(request, "details.html", context)


@login_required(login_url="login")
def vote(request, poll_id):
    update_polls()
    update_elections()

    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll)
    context = {"poll": poll, "choices": choices}
    return render(request, "vote.html", context)


@login_required(login_url="login")
def record_vote(request, poll_id, choice_id):
    update_polls()
    update_elections()

    poll = get_object_or_404(Poll, pk=poll_id)
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
    update_polls()
    update_elections()

    return render(request, "vote_fail.html")


@login_required(login_url="login")
def vote_success(request):
    update_polls()
    update_elections()

    return render(request, "vote_success.html")


@login_required(login_url="login")
def my_votes(request):
    update_polls()
    update_elections()

    votes = Vote.objects.filter(user=request.user)
    ballots = Ballot.objects.filter(user=request.user)
    context = {"votes": votes, "ballots": ballots}
    return render(request, "my_votes.html", context)


@login_required(login_url="login")
def vote_receipt(request, vote_id, choice_visible):
    update_polls()
    update_elections()

    vote = get_object_or_404(Vote, pk=vote_id)
    context = {
        "vote": vote,
        "current_time": timezone.now(),
        "choice_visible": True if choice_visible == 1 else False,
    }
    return render(request, "vote_receipt.html", context)


def register(request):
    update_polls()
    update_elections()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if (
                os.environ.get("AUTOMATICALLY_APPROVE_REGISTRATIONS", default="false")
                != "true"
            ):
                user.is_active = False
                user.save()
            return redirect("register_success")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def register_success(request):
    update_polls()
    update_elections()

    if os.environ.get("AUTOMATICALLY_APPROVE_REGISTRATIONS", default="false") == "true":
        auto_approve = True
    else:
        auto_approve = False

    context = {"auto_approve": auto_approve}
    return render(request, "register_success.html", context)


@login_required(login_url="login")
def elections(request):
    update_polls()
    update_elections()

    elections = Election.objects.all()
    context = {"elections": elections}
    return render(request, "elections.html", context)


@login_required(login_url="login")
def election_vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)

    if request.method == "POST":
        form = ElectionVote(request.POST, candidates=candidates)
        if form.is_valid():
            if not Ballot.objects.filter(user=request.user, election=election).exists():
                ranked_candidates = []
                for i in range(1, len(candidates) + 1):
                    candidate_id = form.cleaned_data[f"rank_{i}"]
                    candidate = Candidate.objects.get(id=candidate_id)
                    ranked_candidates.append(
                        {
                            "rank": i,
                            "candidate_id": candidate.id,
                            "candidate_name": candidate.full_name,
                        }
                    )
                preferences_json = json.dumps(ranked_candidates)
                Ballot.objects.create(
                    user=request.user,
                    election=election,
                    preferences=preferences_json,
                )
                return redirect("vote_success")
            else:
                return redirect("vote_fail")
    else:
        form = ElectionVote(candidates=candidates)

    context = {"form": form, "election": election}

    return render(request, "election_vote.html", context)


@login_required(login_url="login")
def election_details(request, election_id):
    update_polls()
    update_elections()

    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)
    total_votes = len(Ballot.objects.filter(election=election))

    now = timezone.now()
    time_remaining = election.close_date - now
    days, seconds = time_remaining.days, time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_remaining_str = (
        f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    )

    time_until_open = now - election.open_date
    days, seconds = time_until_open.days, time_until_open.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_until_open_str = (
        f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    )

    ballots = Ballot.objects.filter(election=election)
    pyrank_candidates = [
        PyRankCandidate(candidate.full_name) for candidate in candidates
    ]
    pyrank_ballots = []
    for ballot in ballots:
        preferences = json.loads(ballot.preferences)
        ranked_candidates = []
        for i in range(len(preferences)):
            ranked_candidates.append(PyRankCandidate(preferences[i]["candidate_name"]))
        pyrank_ballots.append(PyRankBallot(ranked_candidates=ranked_candidates))
    election_result = pyrankvote.instant_runoff_voting(
        pyrank_candidates, pyrank_ballots
    )

    context = {
        "election": election,
        "candidates": candidates,
        "total_votes": total_votes,
        "time_remaining": time_remaining_str,
        "time_until_open": time_until_open_str,
        "result": election_result,
    }
    return render(request, "election_details.html", context)


@login_required(login_url="login")
def ballot_receipt(request, ballot_id):
    update_polls()
    update_elections()

    ballot = get_object_or_404(Ballot, pk=ballot_id)
    context = {
        "ballot": ballot,
        "current_time": timezone.now(),
    }
    return render(request, "ballot_receipt.html", context)
