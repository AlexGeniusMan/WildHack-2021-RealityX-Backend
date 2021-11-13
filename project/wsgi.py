"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from django.conf import settings
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()


# make request to /api/v1/status to prepare everything for first user request
def make_init_request():
    f = RequestFactory()
    request = f.request(**{
        'wsgi.url_scheme': 'http',
        'HTTP_HOST': '80.78.244.130',
        'QUERY_STRING': '',
        'REQUEST_METHOD': 'POST',
        'PATH_INFO': '/api/predict_hints',
        'SERVER_PORT': '8001',
    })

    def start_response(*args):
        pass

    application(request.environ, start_response)


if os.environ.get('WSGI_FULL_INIT'):
    make_init_request()
