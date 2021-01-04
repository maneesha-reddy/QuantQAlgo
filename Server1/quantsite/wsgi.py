"""
WSGI config for quantsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import eventlet.wsgi
import eventlet
import socketio
from app.views import sio
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quantsite.settings')
application = get_wsgi_application()


application = socketio.WSGIApp(sio, application)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
