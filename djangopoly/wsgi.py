"""
WSGI config for djangopoly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopoly.settings")

from djangopoly import import_env_vars
import_env_vars(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
