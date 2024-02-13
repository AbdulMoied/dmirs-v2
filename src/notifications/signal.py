from notifications.custom_utils import post_notification
from django.db.models.signals import post_save
from notifications.models import Notification
from django.dispatch import receiver


@receiver(post_save, sender=Notification)
def create_notification(sender, instance, created, **kwargs):
    if created:
        post_notification(message_id=instance.id,
                          user_mail="test@gmail.com",
                          message_heading=instance.heading,
                          message=instance.content,
                          message_viewed=instance.viewed)
