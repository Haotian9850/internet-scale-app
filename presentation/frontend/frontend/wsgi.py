"""
WSGI config for templates project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

path = '/app/frontend'
if path not in sys.path:
    sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.settings')

application = get_wsgi_application()

