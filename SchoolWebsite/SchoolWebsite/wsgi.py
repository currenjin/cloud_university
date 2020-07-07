"""
WSGI config for SchoolWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.development'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'SchoolWebsite.settings'
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolWebsite')

application = get_wsgi_application()
