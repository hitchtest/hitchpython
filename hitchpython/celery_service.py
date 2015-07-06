from hitchserve import Service, HitchException
import subprocess
import shutil
import os
import sys

# TODO : Separate out python specific stuff to a parent class. Also specify version of python there?

class CeleryService(Service):
    def __init__(self, version, python, beat=False, app=None, loglevel="INFO", concurrency=2, broker=None, **kwargs):
        self.version = version
        self.python = python
        self.app = app
        self.app_option = [] if app is None else ['--app={}'.format(app), ]

        command = [python, "-u", '-m', 'celery', 'worker', ] \
            + self.app_option \
            + ([] if beat == False else ['--beat', ]) \
            + (['--loglevel={}'.format(loglevel), ]) \
            + ([] if broker is None else ['--broker={}'.format(broker), ]) \
            + (["--concurrency={}".format(concurrency), ])

        kwargs['log_line_ready_checker'] = lambda line: "Connected to" in line
        kwargs['command'] = command
        super(CeleryService, self).__init__(**kwargs)

    @Service.directory.getter
    def directory(self):
        if self._directory is None:
            return self.service_group.project_directory
        else:
            return self._directory

    def setup(self):
        cel_version = "import celery; maj, min, mic, rel, ser = celery.VERSION; print(\"{}.{}.{}\".format(maj, min, mic))"
        try:
            version_output = self.subcommand(self.python, "-c", cel_version).run(check_output=True)
        except OSError as error:
            raise HitchException("Error running celery: {}".format(error))
        if self.version not in version_output:
            raise HitchException("Celery version required is {}, version is {}.".format(self.version, version_output))


    def celery(self, command, ignore_errors=False):
        command = command.split(' ') if type(command) == str else command
        self.run([self.python, "-u", '-m', 'celery', ] + self.app_option + command, ignore_errors=ignore_errors)

    def inspect(self, command):
        command = command.split(' ') if type(command) == str else command
        self.celery(['inspect', ] + command)

    def control(self, command):
        command = command.split(' ') if type(command) == str else command
        self.celery(['inspect', ] + command)

    def status(self):
        self.celery(['status', ])

    def help(self):
        self.celery(['help', ], ignore_errors=True)
