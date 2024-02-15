# database_middleware.py
from django.db import connection
from django.db.utils import OperationalError


class DatabaseCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the database exists
        try:
            with connection.cursor():
                pass  # Do nothing, just checking the connection
        except OperationalError as e:
            # Handle the case where the database doesn't exist
            request.database_exception = e

        response = self.get_response(request)
        return response
