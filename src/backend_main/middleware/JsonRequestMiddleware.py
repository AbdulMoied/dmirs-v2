from backend_main.utils import generic_api_response
import json
import logging

logger = logging.getLogger(__name__)


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
                    return generic_api_response(False, None, 400, response_data)

        response = self.get_response(request)
        return response
