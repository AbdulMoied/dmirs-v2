import hmac

from decouple import config
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Replace with your actual shared secret and header name
        SHARED_SECRET = config("SHARED_SECRET")
        API_KEY_HEADER = config("API_KEY_HEADER", "not-set")

        api_key = request.headers.get(API_KEY_HEADER)

        if not api_key:
            raise AuthenticationFailed("Missing API key")

        is_valid = hmac.compare_digest(api_key.encode('utf-8'), SHARED_SECRET.encode('utf-8'))
        if not is_valid:
            raise AuthenticationFailed("Invalid API key")

        # You can access the validated API key here for further processing
        request.api_key = api_key

        response = self.get_response(request)
        return response
