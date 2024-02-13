from notifications.models import Notification,NotificationStatistics
from django.contrib import admin

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        # "account",
        "heading",
        "content",
        "viewed",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("account__email", 'id', "heading", "created_at")

@admin.register(NotificationStatistics)
class NotificationStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project_count",
        "client_count",
    )
    search_fields = ("id",)