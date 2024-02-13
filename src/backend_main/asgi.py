"""
ASGI config for backend_main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

from channels.routing import URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_main.settings')

django_application = get_asgi_application()
from . import urls 
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(urls.websocket_urlpatterns)
    }
)