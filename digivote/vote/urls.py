from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("auth-success", views.auth_success, name="auth_success"),
    path("polls", views.polls, name="polls"),
    path("details/<int:poll_id>", views.details, name="details"),
    path("vote/<int:poll_id>", views.vote, name="vote"),
    path(
        "record-vote/<int:poll_id>/<int:choice_id>",
        views.record_vote,
        name="record_vote",
    ),
    path("success", views.vote_success, name="vote_success"),
    path("fail", views.vote_fail, name="vote_fail"),
    path("my-votes", views.my_votes, name="my_votes"),
]
