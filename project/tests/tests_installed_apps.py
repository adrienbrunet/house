from django.conf import settings


def test_installed_apps():
    apps = {
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework.authtoken",
        "rest_framework_swagger",
        "apps.houses.apps.HousesConfig",
    }
    assert apps.issubset(settings.INSTALLED_APPS), settings.INSTALLED_APPS
