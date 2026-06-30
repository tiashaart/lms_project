"""
WSGI config for HALMS project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'halms.settings')

application = get_wsgi_application()
