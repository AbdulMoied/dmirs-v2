"""backend_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from notifications.consumers import NotificationConsumer, NotificationStatisticsConsumer

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Sunset-Backend API",
        default_version='v1',
        description="This is a documentation for all the endpoints available for Sunset Backend.",
        license=openapi.License(name="Horizon Digital"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

websocket_urlpatterns = [
    path("ws/notifications/<str:user_mail>/", NotificationConsumer.as_asgi()),
    path("ws/notification_statistics/", NotificationStatisticsConsumer.as_asgi()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    # URLs for LogIn & Logout API
    path('api/', include('authentication.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('projects.urls')),
    path('api/', include('dashboard.urls')),
    # URLs for API documentation
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api-docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # URLS for websocket
    path("ws/", include(websocket_urlpatterns)),
]

admin.site.site_header = "SUNSET BACKEND"
