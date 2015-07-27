HitchPython
===========

HitchPython is a plugin for the Hitch test framework that lets you test
python programs. Specifically, it includes code to:

* Download, build and create a virtualenv from all versions of python.
* Run a Django runserver service using hitchserve_.
* Run a Celery service using hitchserve_.

The Django runserver service will:

* Optionally, run migrations and insert a site into django_sites table, prior to starting the service.
* Install fixtures.
* Run on a specific port.
* Get the URL.
* Generate a runnable manage subcommand.

Documentation
=============

See:

* https://hitchtest.readthedocs.org/en/latest/services/django.html
* https://hitchtest.readthedocs.org/en/latest/services/celery.html
* https://hitchtest.readthedocs.org/en/latest/api/package_api.html
