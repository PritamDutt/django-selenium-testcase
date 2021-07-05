from django.apps import AppConfig


class SeleniumTestcaseConfig(AppConfig):
    name = "selenium_testcase"
    # https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
    # Set default autofield to "django.db.models.AutoField" for apps created prior to Django 3.2
    default_auto_field = "django.db.models.AutoField"
