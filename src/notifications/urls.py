# notifications/urls.py
from django.urls import path
from .views import NotificationList

urlpatterns = [
    path('notifications/', NotificationList.as_view(), name='notification-list'),
    # Add more URL patterns as needed
]
