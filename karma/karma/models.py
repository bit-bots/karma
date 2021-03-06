from django.contrib.auth.models import User, Group
from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=50, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    karma_rules = models.TextField(max_length=400, default='No special rules')

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        unique_together = ['name', 'project']
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class KarmaPoints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    time = models.DateTimeField()
    points = models.IntegerField()
    description = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
