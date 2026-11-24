from django.apps import AppConfig


class KarmaConfig(AppConfig):
    name = "karma.karma"
    # Preserve the primary key type in the existing migration history.
    default_auto_field = "django.db.models.AutoField"
