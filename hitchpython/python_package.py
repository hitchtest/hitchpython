from subprocess import call, check_output, PIPE, STDOUT
from os import chdir, makedirs, getcwd, path
from hitchtest import HitchPackage, utils
import python_build
import shutil
import sys

ISSUES_URL = "http://github.com/hitchtest/hitchpython/issues"

class PythonPackage(HitchPackage):
    name = "Python"

    PYTHON_VERSIONS = [
        '2.1.3', '2.2.3', '2.3.7', '2.4', '2.4.1', '2.4.2', '2.4.3', '2.4.4', '2.4.5', '2.4.6',
        '2.5', '2.5.1', '2.5.2', '2.5.3', '2.5.4', '2.5.5', '2.5.6',
        '2.6.6', '2.6.7', '2.6.8', '2.6.9',
        '2.7', '2.7.1', '2.7.2', '2.7.3', '2.7.4',
        '2.7.5', '2.7.6', '2.7.7', '2.7.8', '2.7.9', '2.7.10', '2.7-dev',
        '3.0.1', '3.1-dev', '3.1', '3.1.1', '3.1.2', '3.1.3', '3.1.4', '3.1.5',
        '3.2', '3.2.1', '3.2.2', '3.2.3', '3.2.4', '3.2.5', '3.2.6','3.2-dev',
        '3.3.0', '3.3-dev', '3.3.1', '3.3.2', '3.3.3', '3.3.4', '3.3.5', '3.3.6',
        '3.4.0', '3.4-dev', '3.4.1', '3.4.2', '3.4.3', '3.5.0b1',
        '3.5.0b2', '3.5.0b3', '3.5-dev',
    ]

    def __init__(self, python_version="2.7.10", directory=None, bin_directory=None):
        super(PythonPackage, self).__init__()
        self.python_version = self.check_version(
            python_version, self.PYTHON_VERSIONS, ISSUES_URL, name="Python"
        )

        if directory is None:
            self.directory = path.join(self.get_build_directory(), "python{}".format(self.python_version))
        else:
            self.directory = directory
        self.bin_directory = bin_directory


    def build(self):
        """Download and compile the specified version of python."""
        if not path.exists(self.directory):
            python_build.build.python_build(self.python_version, self.directory)
        self.bin_directory = path.join(self.directory, "bin")

    def verify(self):
        """Verify the package exists and is working."""
        output = check_output([self.python, "--version"], stderr=STDOUT).decode('utf8')

        if self.python_version not in output:
            raise RuntimeError(
                "python --version returned '{}', expecting version '{}'".format(output, self.python_version)
            )

    @property
    def python(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return path.join(self.bin_directory, "python")

    @property
    def pip(self):
        if self.bin_directory is None:
            raise RuntimeError("bin_directory not set.")
        return path.join(self.bin_directory, "pip")
