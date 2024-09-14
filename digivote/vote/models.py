from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Poll(models.Model):
    poll_text = models.CharField(max_length=512)
    publish_date = models.DateTimeField("date published")
    poll_open = models.BooleanField(default=True)

    def __str__(self):
        return self.poll_text

    def get_votes(self):
        return User.objects.filter(vote__poll=self)


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
