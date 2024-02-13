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
