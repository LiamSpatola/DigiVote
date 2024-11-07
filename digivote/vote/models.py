from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def get_default_close_date():
    return timezone.now() + timedelta(days=1)


# Create your models here.
class Poll(models.Model):
    poll_text = models.CharField(max_length=512)
    voting_instructions = models.CharField(max_length=4096)
    publish_date = models.DateTimeField("date published", default=timezone.now)
    poll_open = models.BooleanField(default=True)
    open_date = models.DateTimeField("open date", default=timezone.now)
    close_date = models.DateTimeField("close date", default=get_default_close_date)
    visible = models.BooleanField(default=True)
    results_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.poll_text

    def get_votes(self):
        return User.objects.filter(vote__poll=self)

    def update_status(self):
        if timezone.now() >= self.close_date:
            self.poll_open = False
        elif timezone.now() >= self.open_date:
            self.poll_open = True
        else:
            self.poll_open = False

        self.save()


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=256)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "poll")

    def __str__(self):
        return f"User: {self.user} Choice: {self.choice} Poll: {self.poll}"


class Election(models.Model):
    election_name = models.CharField(max_length=512)
    voting_instructions = models.CharField(max_length=4096)
    publish_date = models.DateTimeField("date published", default=timezone.now)
    election_open = models.BooleanField(default=True)
    election_type = models.CharField(
        choices=[
            ("IRV", "Instant Runoff Voting"),
            ("STV", "Single Transferable Vote"),
            ("PBV", "Preferential Block Voting"),
        ],
        max_length=3,
        default="IRV",
    )
    number_of_seats = models.IntegerField(default=1)
    open_date = models.DateTimeField("open date", default=timezone.now)
    close_date = models.DateTimeField("close date", default=get_default_close_date)
    visible = models.BooleanField(default=True)
    results_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.election_name

    def update_status(self):
        if timezone.now() >= self.close_date:
            self.election_open = False
        elif timezone.now() >= self.open_date:
            self.election_open = True
        else:
            self.election_open = False

        self.save()

    def clean(self):
        super().clean()

        if self.election_type == "IRV" and self.number_of_seats > 1:
            raise ValidationError(
                "Instant Runoff Voting can only be used for single-seat elections."
            )


class Ballot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    preferences = models.JSONField()
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "election")


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=256)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
