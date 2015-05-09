"""
WSGI config for sigepro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sigepro.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

sys.path = ['/var/www/sigepro'] + sys.path

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
