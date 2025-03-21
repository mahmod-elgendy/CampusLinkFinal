#!/usr/bin/env python
import os
import sys

import django
from django.core.management import execute_from_command_line

try:
    django.setup()  # This is the recommended way to configure settings in manage.py
except django.core.exceptions.ImproperlyConfigured:
    # Handle configuration errors here (optional)
    pass

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)