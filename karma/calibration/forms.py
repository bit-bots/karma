from django.forms import ModelForm

from karma.calibration.models import Calibration


class CalibrationForm(ModelForm):
    class Meta:
        model = Calibration
        fields = ('start_day', 'end_day', 'percent')
