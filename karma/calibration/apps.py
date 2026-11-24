from django.apps import AppConfig


class CalibrationConfig(AppConfig):
    name = "karma.calibration"
    # Preserve the primary key type in the existing migration history.
    default_auto_field = "django.db.models.AutoField"
