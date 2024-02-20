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
            # If an exception occurred during request processing, handle it
            return self.process_exception(request, e)

        # Continue with your existing logic for non-exception responses
        if response.status_code == 401:
            data = {'details': 'Unauthorized Request'}
            return generic_api_response(False, None, 401, data)
        if response.status_code == 403:
            data = {'details': 'You do not have permission to perform this action.'}
            return generic_api_response(False, None, 401, data)
        if response is None:
            return generic_api_response(False, None, 400, 'Unknown error')
        if response.status_code == 404:
            # If it's a 404 response and the content is not empty, return the response as is
            if response.content or response.streaming:
                return response
            data = {'details': 'Resources not found'}
            return generic_api_response(False, None, 404, data)
        if response.status_code == 500:
            data = {'details': 'Internal server error'}
            return generic_api_response(False, None, 500, data)

        return response

    def process_exception(self, request, exception):
        message = str(exception) if exception else 'Unknown error'
        return generic_api_response(False, None, 400, message)
