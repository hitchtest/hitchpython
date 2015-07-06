from hitchserve import Service
import contextlib
import subprocess
import shutil
import json
import sys
import os

# TODO : Python service with lines of code covered, etc.
# TODO : Django fixtures + django settings fixtures.
# TODO : Handle runserver_plus?
# TODO : Add options that you can run with runserver.

class DjangoService(Service):
    def __init__(self, version, python, port=18080, managepy=None, settings=None, fixtures=None, verbosity=1, sites=True, migrations=True, **kwargs):
        self.version = version
        self.python = python
        self.verbosity = verbosity if 0 <= verbosity <= 3 else 1
        self.port = port
        self.django_fixtures = [] if fixtures is None else fixtures
        self.settings = settings
        self.migrations = migrations
        self.sites = sites
        self.managepy = managepy
        self.settings_option = [] if settings is None else ['--settings=' + settings, ]
        kwargs['log_line_ready_checker'] = lambda line: "Quit the server with CONTROL-C." in line
        super(DjangoService, self).__init__(**kwargs)

    @Service.directory.getter
    def directory(self):
        if self._directory is None:
            return self.service_group.project_directory
        else:
            return self._directory

    @Service.command.getter
    def command(self):
        if self._command is None:
            return [
                self.python, "-u", self.managepy, 'runserver', str(self.port),
                '--verbosity', str(self.verbosity), '--noreload',
            ] + self.settings_option
        else:
            return self._command

    @property
    def managepy(self):
        if self._managepy is None:
            return self.service_group.project_directory + os.sep + 'manage.py'
        else:
            return self._managepy

    @managepy.setter
    def managepy(self, value):
        self._managepy = value

    def setup(self):
        os.chdir(self.directory)
        self.log("Checking Django version...")
        version_output = self.subcommand(self.python, "-c", "import django; print(django.get_version())").run(check_output=True)
        if self.version not in version_output:
            raise RuntimeError("Django version needed is {}, output is {}.".format(self.version, version_output))

        # TODO: For earlier version than 1.8, run syncdb
        #self.log("Syncing database...")
        #self.manage("syncdb", "--noinput").run()
        if self.migrations:
            self.log("Running migrations...")
            self.manage("migrate").run()
        if self.sites:
            self.log("Updating sites table...")
            sites = json.dumps([{
                "pk": 1,
                "model": "sites.site",
                "fields": {
                    "domain": "127.0.0.1:{}".format(self.port),
                    "name": "127.0.0.1:{}".format(self.port),
                }
            }])
            sites_dir = self.service_group.hitch_dir.hitch_dir
            with open("{}/sites.json".format(sites_dir), "w") as sites_fixture_handle:
                sites_fixture_handle.write(sites)
            self.manage("loaddata", sites_dir + os.sep + "sites.json").run()
        for fixture in self.django_fixtures:
            self.log("manage.py loaddata {}".format(fixture))
            self.manage("loaddata", fixture).run()

    def manage(self, *args):
        """Run Django manage subcommands."""
        manage_args = [self.python, "-u", self.managepy, ] + list(args) + self.settings_option
        return self.subcommand(*manage_args)

    def url(self):
        """Return a URL for the Django site."""
        return "http://127.0.0.1:{}".format(self.port)

    def savefixture(self, filename):
        """Saves a JSON database fixture."""
        self.manage("dumpdata", filename).run()

    #@contextlib.contextmanager
    #def context_models(self):
        #import django
        #if django.VERSION[:2] < (1, 7):
            #raise RuntimeError("Cannot import models for versions of django below 1.7")
        #elif django.VERSION[:2] >= (1, 7):
            #os.chdir(self.directory)
            #sys.path.append(self.directory)
            #old_django_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "")
            #os.environ['DJANGO_SETTINGS_MODULE'] = '' if self.settings is None else self.settings
            #django.setup()
            #yield {x.__module__ + '.' + x.__name__:x for x in django.apps.apps.get_models()}
            #os.environ['DJANGO_SETTINGS_MODULE'] = old_django_settings_module
