from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.addresses.urls")),
    path("", include("apps.contact.urls")),
]


if settings.DEBUG:
    from django.views import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from rest_framework_swagger.views import get_swagger_view

    schema_view = get_swagger_view(title="Housing api")

    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(
        [
            path("swagger/", schema_view),
            path("api-auth/", include("rest_framework.urls")),
            path(
                "favicon.ico",
                static.serve,
                {"document_root": settings.STATIC_ROOT, "path": "favicon.ico"},
            ),
            re_path(
                r"^media/(?P<path>.*)$",
                static.serve,
                {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
            ),
        ]
    )
