from django.conf import settings
from django.db import models


class Calibration(models.Model):
    start_day = models.DateField()
    end_day = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    percent = models.IntegerField()
