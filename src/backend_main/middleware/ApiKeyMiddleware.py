import hmac
from decouple import config
import logging
from backend_main.utils import generic_api_response

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
            error = {'details': 'Missing API key'}
            return generic_api_response(False, None, 401, error)
        is_valid = hmac.compare_digest(api_key.encode('utf-8'), SHARED_SECRET.encode('utf-8'))

        if not is_valid:
            error = {'details': 'Invalid API key'}
            return generic_api_response(False, None, 401, error)

        # You can access the validated API key here for further processing
        request.api_key = api_key

        response = self.get_response(request)
        return response
