from django.forms import ModelForm

from karma.karma.models import KarmaPoints, Project, Category


class KarmaPointsForm(ModelForm):
    class Meta:
        model = KarmaPoints
        fields = ['description', 'points', 'project', "category"]


class KarmaProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'user', 'group']


class KarmaCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'project']
