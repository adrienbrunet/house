import pytest
import importlib
import project.urls

from django.urls.resolvers import RegexPattern, URLResolver


"""
With the many views tests, we know for a fact
our urls are working as it should be.

What we test here is we do have static file urls in debug.
"""


@pytest.fixture
def path_solver(settings):
    settings.DEBUG = True
    importlib.reload(project.urls)
    return URLResolver(RegexPattern(""), "project.urls")


def test_url_static(path_solver):
    assert path_solver.resolve("static/path")


def test_url_media(path_solver):
    assert path_solver.resolve("media/path")
