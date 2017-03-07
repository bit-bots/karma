from django.contrib.auth.models import User, Group
from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class KarmaPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    time = models.DateTimeField()
    points = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    category = models.ForeignKey(Category)
