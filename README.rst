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

Install
=======

Install the module like so::

    $ hitch install hitchpython


Build a virtualenv
==================

.. code-block:: python

    import hitchpython

    def set_up(self):
        python_package = hitchpython.PythonPackage(
            python_version="2.7.10",
            directory=os.path.join(PROJECT_DIRECTORY, "py2710")
        )
        python_package.build()
        python_package.verify()
        # virtualenv.python now points to a usable python interpreter


.. code-block:: python

    import hitchpython

    def set_up(self):
        self.services['Django'] = hitchdjango.DjangoService(
            version="1.8",                                              # Mandatory
            python=python_package.python,                               # Mandatory
            managepy=None,                                              # Optional full path to manage.py (default: None, assumes in project directory)
            django_fixtures=['fixture1.json',],                         # Optional (default: None)
            port=18080,                                                 # Optional (default: 18080)
            settings="remindme.settings",                               # Optional (default: settings)
            needs=[self.services['Postgres'], ]                         # Optional (default: no prerequisites)
        )


        # Interact during the test:
        >>> self.services['Django'].manage("help").run()
        [ Prints help ]

        >>> self.services['Django'].url()
        http://127.0.0.1:18080/

        >>> self.services['Django'].savefixture("fixtures/database_current_state.json").run()
        [ Saves fixture ]


See this service in action at the DjangoRemindMe_ project.


.. _HitchServe: https://github.com/hitchtest/hitchserve
.. _DjangoRemindMe: https://github.com/hitchtest/django-remindme
