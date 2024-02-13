import itertools

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def get_portal_permissions(permissions,user_permissions,screens,actions):
    
    permissions_list = list(permissions.values_list("codename", flat=True))
    print(screens)
    for screen, action in itertools.product(screens.items(), actions.items()):
        # check if the user has permission to access the screen and action
        if f"view_{screen[0]}" in permissions_list or f"add_{screen[0]}" in permissions_list or f"change_{screen[0]}" in permissions_list or f"delete_{screen[0]}" in permissions_list:
            # Create a new dictionary
            screen_action = {"screen_id": screen[1], "action_id": action[1]}
            # Add the dictionary to the list
            user_permissions.append(screen_action)

def send_reset_password_email(context):
        email_html_message = render_to_string(
        'email/user_reset_password.html',context)
        email = EmailMessage(
            'Reset Password Request', email_html_message,settings.DEFAULT_FROM_EMAIL, context['to_email'])
        email.content_subtype = 'html'
        email.send()

