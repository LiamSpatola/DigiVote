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
from .models import Ballot, Candidate, Choice, Election, Poll, Vote, VoteRecord, BallotRecord

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

    polls_already_voted_in = []
    for poll in Poll.objects.all():
        if VoteRecord.objects.filter(user=request.user, poll=poll).exists():
            polls_already_voted_in.append(poll)

    polls = Poll.objects.all()
    context = {"polls": polls, "polls_already_voted_in": polls_already_voted_in}
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

    context = {
        "poll": poll,
        "choices": choices_with_percentage,
        "winners": winners,
        "total_votes": total_votes,
    }
    return render(request, "details.html", context)


@login_required(login_url="login")
def vote(request, poll_id):
    update_polls()
    update_elections()

    poll = get_object_or_404(Poll, pk=poll_id)
    user_has_voted = VoteRecord.objects.filter(user=request.user, poll=poll).exists()
    choices = Choice.objects.filter(poll=poll)
    context = {"poll": poll, "choices": choices}

    if user_has_voted:
        return redirect("vote_fail")
    else:
        return render(request, "vote.html", context)


@login_required(login_url="login")
def record_vote(request, poll_id, choice_id):
    update_polls()
    update_elections()

    poll = get_object_or_404(Poll, pk=poll_id)
    choice = get_object_or_404(Choice, pk=choice_id, poll=poll)
    user_has_voted = VoteRecord.objects.filter(user=request.user, poll=poll).exists()
    if user_has_voted or not poll.poll_open:
        return redirect("vote_fail")
    else:
        Vote.objects.create(choice=choice, poll=poll)
        VoteRecord.objects.create(user=request.user, poll=poll)
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

    votes = VoteRecord.objects.filter(user=request.user)
    ballots = BallotRecord.objects.filter(user=request.user)
    context = {"votes": votes, "ballots": ballots}
    return render(request, "my_votes.html", context)


@login_required(login_url="login")
def vote_receipt(request, vote_id):
    update_polls()
    update_elections()

    vote = get_object_or_404(VoteRecord, pk=vote_id)
    context = {
        "vote": vote,
        "current_time": timezone.now(),
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

    elections_already_voted_in = []
    for election in Election.objects.all():
        if BallotRecord.objects.filter(user=request.user, election=election).exists():
            elections_already_voted_in.append(election)

    elections = Election.objects.all()
    context = {
        "elections": elections,
        "elections_already_voted_in": elections_already_voted_in,
    }
    return render(request, "elections.html", context)


@login_required(login_url="login")
def election_vote(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)
    user_has_voted = BallotRecord.objects.filter(
        user=request.user, election=election
    ).exists()

    if request.method == "POST":
        form = ElectionVote(request.POST, candidates=candidates)
        if form.is_valid():
            if not BallotRecord.objects.filter(user=request.user, election=election).exists():
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
                    election=election,
                    preferences=preferences_json,
                )
                BallotRecord.objects.create(user=request.user, election=election)
                return redirect("vote_success")
            else:
                return redirect("vote_fail")
    else:
        form = ElectionVote(candidates=candidates)

    context = {"form": form, "election": election}

    if user_has_voted:
        return redirect("vote_fail")
    else:
        return render(request, "election_vote.html", context)


@login_required(login_url="login")
def election_details(request, election_id):
    update_polls()
    update_elections()

    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)
    total_votes = len(Ballot.objects.filter(election=election))

    ballots = Ballot.objects.filter(election=election)
    pyrank_candidates = [
        PyRankCandidate(candidate.full_name) for candidate in candidates
    ]
    pyrank_ballots = []

    first_preferences = dict()
    for candidate in candidates:
        first_preferences[candidate.full_name] = 0

    for ballot in ballots:
        preferences = json.loads(ballot.preferences)
        ranked_candidates = []
        for i in range(len(preferences)):
            ranked_candidates.append(PyRankCandidate(preferences[i]["candidate_name"]))
        pyrank_ballots.append(PyRankBallot(ranked_candidates=ranked_candidates))

        preferred_candidate = preferences[0]["candidate_name"]
        first_preferences[preferred_candidate] += 1

    match election.election_type:
        case "IRV":
            election_result = pyrankvote.instant_runoff_voting(
                pyrank_candidates, pyrank_ballots
            )
        case "STV":
            election_result = pyrankvote.single_transferable_vote(
                pyrank_candidates,
                pyrank_ballots,
                number_of_seats=election.number_of_seats,
            )
        case "PBV":
            election_result = pyrankvote.preferential_block_voting(
                pyrank_candidates,
                pyrank_ballots,
                number_of_seats=election.number_of_seats,
            )

    candidates_with_percentages = []
    for candidate, vote in first_preferences.items():
        if total_votes > 0:
            vote_percentage = round((vote / total_votes) * 100, 2)
        else:
            vote_percentage = 0

        candidates_with_percentages.append(
            {"name": candidate, "votes": vote, "vote_percentage": vote_percentage}
        )

    highest_first_preference_vote = max(first_preferences.values())
    first_preference_winner = [
        candidate
        for candidate, vote in first_preferences.items()
        if vote == highest_first_preference_vote
    ]

    context = {
        "election": election,
        "candidates": candidates,
        "candidates_with_percentages": candidates_with_percentages,
        "first_preference_winners": first_preference_winner,
        "total_votes": total_votes,
        "result": election_result,
    }
    return render(request, "election_details.html", context)


@login_required(login_url="login")
def ballot_receipt(request, ballot_id):
    update_polls()
    update_elections()

    ballot = get_object_or_404(BallotRecord, pk=ballot_id)
    context = {
        "ballot": ballot,
        "current_time": timezone.now(),
    }
    return render(request, "ballot_receipt.html", context)
