# from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from authentication.models import Account
# from django.conf import settings
# import datetime
import uuid
# import jwt


# email to UUID generator
def mail_to_uuid(user_mail):
    return uuid.uuid3(uuid.NAMESPACE_URL, user_mail).hex


# post notification to specified channel
def post_notification(message_id, user_mail, message_heading, message, message_viewed,
                      **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        mail_to_uuid(user_mail=user_mail),
        {
            "type": "notify",
            "id": message_id,
            "message_heading": message_heading,
            "message": message,
            "message_viewed": message_viewed,

        }
    )
    return True