from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import random
import string

def send_mail_to_user(context):
    if settings.ENVIRONMENT == 'Development':
        context['URL'] = settings.FRONTEND_DEV_URL
    else:
        context['URL'] = settings.FRONTEND_PROD_URL
    email_html_message = render_to_string(
        'email/send_user_credentials.html',context)
    
    email = EmailMessage(
        "User Credentials",
        email_html_message,
        settings.DEFAULT_FROM_EMAIL,
        [context['email']]
    )
    email.content_subtype = 'html'
    email.send()

def send_new_password_to_employee(context):
    if settings.ENVIRONMENT == 'Development':
        context['URL'] = settings.FRONTEND_DEV_URL
    else:
        context['URL'] = settings.FRONTEND_PROD_URL
    email_html_message = render_to_string(
        'email/employee_new_password_mail.html',context)
    
    email = EmailMessage(
        "User Credentials",
        email_html_message,
        settings.DEFAULT_FROM_EMAIL,
        [context['email']]
    )
    email.content_subtype = 'html'
    email.send()


def send_reset_password_email(context):
        email_html_message = render_to_string(
        'email/user_reset_password.html',context)
        email = EmailMessage(
            'Reset Password Request', email_html_message,settings.DEFAULT_FROM_EMAIL, context['to_email'])
        email.content_subtype = 'html'
        email.send()

import random
import string
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for i in range(8))
    return password