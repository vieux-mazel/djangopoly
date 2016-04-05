"""
WSGI config for djangopoly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import glob
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopoly.settings")

def import_env_vars(directory):
    """
    List the files present in the given directory and for each of them create
    an environment variable named after the file, and which value is the
    contents of the file.
    """
    env_vars = glob.glob(os.path.join(directory, '*'))

    for env_var in env_vars:
        with open(env_var, 'r') as env_var_file:
            os.environ.setdefault(env_var.split(os.sep)[-1],
                                  env_var_file.read().strip())

import_env_vars(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
