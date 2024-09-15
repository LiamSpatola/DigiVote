from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta


def get_default_close_date():
    return timezone.now() + timedelta(days=1)

# Create your models here.
class Poll(models.Model):
    poll_text = models.CharField(max_length=512)
    publish_date = models.DateTimeField("date published", default=timezone.now)
    poll_open = models.BooleanField(default=True)
    close_date = models.DateTimeField("close date", default=get_default_close_date)

    def __str__(self):
        return self.poll_text

    def get_votes(self):
        return User.objects.filter(vote__poll=self)
    
    def update_status(self):
        if timezone.now() >= self.close_date:
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
