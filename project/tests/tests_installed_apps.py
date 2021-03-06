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
        "apps.housing.apps.HousingConfig",
        "apps.users.apps.UsersConfig",
        "apps.addresses.apps.AddressesConfig",
        "apps.contact.apps.ContactConfig",
        "apps.groups.apps.GroupsConfig",
        "apps.bookings.apps.BookingsConfig",
    }
    assert apps.issubset(settings.INSTALLED_APPS), settings.INSTALLED_APPS
