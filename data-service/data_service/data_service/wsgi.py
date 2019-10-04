"""
WSGI config for data_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/app/data_service'
if path not in sys.path:
    sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_service.settings')

application = get_wsgi_application()