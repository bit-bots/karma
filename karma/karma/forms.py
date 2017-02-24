from django.forms import ModelForm

from karma.karma.models import KarmaPoints


class KarmaPointsForm(ModelForm):
    class Meta:
        model = KarmaPoints
        fields = ['description', 'points']

