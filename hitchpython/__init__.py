from hitchpython.django_service import DjangoService
from hitchpython.celery_service import CeleryService
from hitchpython.python_package import PythonPackage


UNIXPACKAGES = [
    "libreadline6", "libreadline6-dev", "zlib1g-dev", "libxml2",
    "libxml2-dev", "libssl-dev", "libbz2-dev", "libsqlite3-dev",
    "sqlite3", "patch",
]
