# middleware.py

import logging
import json

from django.http import JsonResponse
logger = logging.getLogger(__name__)

from .utils import generic_api_response


from .utils import generic_api_response


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            message = str(e) if e else 'Unknown error'
            return generic_api_response(False, None, 400, message)

        if response is None:
            return generic_api_response(False, None, 400, 'Unknown error')
        if response.status_code == 404:
            data = {'details': 'Resource not found'}
            return generic_api_response(False, None, 404, data)
        if response.status_code == 500:
            data = {'details': 'Internal server error'}
            return generic_api_response(False, None, 500, data)
        return response

    def process_exception(self, request, exception):
        message = str(exception) if exception else 'Unknown error'
        return generic_api_response(False, None, 400, message)






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
