#!/usr/bin/env python
import os
import sys
from djangopoly import import_env_vars

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangopoly.settings.base")

    import_env_vars(os.path.join(os.path.dirname(__file__), 'env'))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
