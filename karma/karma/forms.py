from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from karma.karma.models import KarmaPoints, Project, Category


class KarmaPointsForm(ModelForm):
    class Meta:
        model = KarmaPoints
        fields = ['description', 'points', 'project', "category", "time"]
        widgets = {
            'time': DateTimeWidget(attrs={'id': "time"}, usel10n = True, bootstrap_version=3)
        }


class KarmaProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'user', 'group', 'karma_rules']


class KarmaCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'project']
