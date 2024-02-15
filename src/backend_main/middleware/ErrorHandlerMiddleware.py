from backend_main.utils import generic_api_response
import logging

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            message = str(e) if e else 'Unknown error'
            return generic_api_response(False, None, 400, message)
        if response.status_code == 401:
            data = {'details': 'Unauthorized Request'}
            return generic_api_response(False, None, 500, data)
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
