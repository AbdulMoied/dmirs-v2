# middleware.py

import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log the exception
            logger.exception("An error occurred: %s", str(e))

            # Handle the exception gracefully (e.g., redirect to an error page)
            # Modify this part based on your application's requirements

            response = render(request, 'error_page.html', {'error_message': str(e)}, status=500)

        return response



import json

from django.http import JsonResponse


class JsonRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.content_type
            if content_type == "application/json":
                try:
                    # Parse the JSON data from the request body
                    request.json_data = json.loads(request.body.decode('utf-8'))
                except json.JSONDecodeError:
                    # Handle invalid JSON data gracefully
                    response_data = {'error': 'Invalid JSON data in request body'}
                    response = JsonResponse(response_data, status=400)
                    return response

        response = self.get_response(request)
        return response
