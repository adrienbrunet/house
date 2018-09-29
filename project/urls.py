from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path


urlpatterns = [path("admin/", admin.site.urls)]


if settings.DEBUG:
    from os.path import join
    from django.views import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(
        [
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
