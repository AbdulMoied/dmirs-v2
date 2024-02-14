import os
import sys
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler
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
def generic_api_response(success=False, data=None, status=200, error=None, **kwargs):
    # define a standard response format
    if success is True:
        response_data = {
            'success': success,
            'payload': data,
        }
    else:
        response_data = {
            'success': success,
            'errors': error,
        }

        # add any additional fields to the response data
    response_data.update(kwargs)

    # return a JSON response with the standardized format and status code
    return JsonResponse(response_data, status=status)

import random
import string

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Check if the response is None
    if response is None:
        # Handle the case where there is no response
        return generic_api_response(False, None, status=500, error={"detail": "An error occurred"})

    # Now add the HTTP status code to the response.
    return generic_api_response(False, None, response.status_code, response.data)

def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for i in range(8))
    return password

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'per_page'
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'payload': {'data': data},
            'paging': {
                'current_page': self.page.number - 1,
                'last_page': self.page.paginator.num_pages - 1,
                'per_page': self.page.paginator.per_page,
                'current_items': self.page.end_index() - self.page.start_index() + 1,
                'from': self.page.start_index(),
                'to': self.page.end_index(),
                'total': self.page.paginator.count,
            }
        })
