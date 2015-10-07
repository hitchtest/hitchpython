# -*- coding: utf-8 -*
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
import subprocess
import codecs
import sys
import os


class CustomInstall(install):
    def run(self):
        try:
            import unixpackage
            unixpackage.install([
                "libreadline6", "libreadline6-dev", "zlib1g-dev", "libxml2", "libxml2-dev",
                "libssl-dev", "libbz2-dev", "libsqlite3-dev", "sqlite3", "patch"
            ], polite=True)
        except ImportError:
            sys.stderr.write("WARNING : unixpackage unavailable; cannot check for system dependencies.")
            sys.stderr.flush()
        install.run(self)

def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

setup(name="hitchpython",
      version="0.3.9",
      description="Hitch plug-in to test python programs, including Celery and Django.",
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: Unix',
          'Framework :: Django',
          'Framework :: Django :: 1.8',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='hitch testing framework bdd tdd declarative tests testing service django celery python',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      url='https://hitchtest.readthedocs.org/',
      license='AGPL',
      install_requires=['hitchserve', 'hitchtest', 'python-build', ],
      packages=find_packages(exclude=[]),
      package_data={},
      zip_safe=False,
      include_package_data=True,
      cmdclass={'install': CustomInstall},
)
