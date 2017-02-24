from django.contrib.auth.models import User
from django.db import models


class KarmaPoints(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField()
    description = models.CharField(max_length=200)

