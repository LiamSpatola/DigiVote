from django.db import models

# Create your models here.
class Poll(models.Model):
    poll_text = models.CharField(max_length=512)
    publish_date = models.DateTimeField('date published')
    poll_open = models.BooleanField(default=True)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=256)
    votes = models.IntegerField(default=0)