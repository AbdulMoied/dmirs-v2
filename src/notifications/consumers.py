from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification, NotificationStatistics
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notification_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notification_group", self.channel_name)

    async def notification_count(self, event):
        message = event.get("message", "New Project Created")
        count = event.get("count", 0)
        await self.send(text_data=json.dumps({"message": message, "project_count": count}))

    @receiver(post_save, sender=Notification)
    def send_notification_update(sender, instance, created, **kwargs):
        if not created:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_group",
                {"type": "notification.count", "message": "New Project Created",
                 "count": instance.account.project_count}
            )


class NotificationStatisticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("notification_statistics_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notification_statistics_group", self.channel_name)

    async def notification_statistics(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps({"notification_statistics": data}))

    @receiver(post_save, sender=NotificationStatistics, dispatch_uid='unique_identifier')
    def send_notification_statistics_update(sender, instance, created, **kwargs):
        if created:
            statistics_data = {
                "project_count": instance.project_count,
                "client_count": instance.client_count,
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notification_statistics_group",
                {"type": "notification.statistics", "data": statistics_data}
            )
