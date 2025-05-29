"""
WSGI config for salvador_expoe project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salvador_expoe.settings')

application = get_wsgi_application() 