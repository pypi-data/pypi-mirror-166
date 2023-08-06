from django.apps import AppConfig


class WagtailHoneypotTestAppConfig(AppConfig):
    label = "wagtail_honeypot_test"
    name = "wagtail_honeypot.test"
    verbose_name = "Wagtail Honeypot tests"

    default_auto_field = "django.db.models.AutoField"
