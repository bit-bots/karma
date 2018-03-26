from django.contrib import admin

from .models import KarmaPoints, Project, Category

admin.site.register(KarmaPoints)
admin.site.register(Category)
admin.site.register(Project)
