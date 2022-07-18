"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings.setting_secrets import settings_location


os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_location)

application = get_wsgi_application()
