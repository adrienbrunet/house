# House

This is an API to handle a small personnal project where one can manage its housing. It will handle bookings, faq and more to come.
It is hosted on [github](https://github.com/adrienbrunet/house).

API is build on top of [Django](https://www.djangoproject.com/) and [drf](http://www.django-rest-framework.org/).

Requirements: python3 & pipenv 🐍 ✨

## Install

`pipenv --three`

`pipenv install`

`python manage.py migrate` to setup your database.

`python manage.py runserver` to launch a local development server.

## Format

Code formatting is ensured with [black](https://black.readthedocs.io/en/stable/).

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Tests ✅

Unit and integration tests use [pytest](https://docs.pytest.org/en/latest/).

They can be run with the following command: `pytest`

## Logging

Classic django logs has been kept.
"Audit" log has been added to monitor some actions or build some metrics.
It's base on systemd and thus journalctl.

You can access these logs with the following command:

`journalctl -t django-audit`
