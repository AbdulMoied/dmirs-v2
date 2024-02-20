from django.http import JsonResponse
from backend_main.utils import generic_api_response


class ParameterCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for required parameters in the request
        required_parameters = ['db_identifier']

        # Determine where to check parameters based on the request method
        if request.method in ['GET', 'DELETE']:
            request_data = request.GET
        elif request.method in ['POST', 'PUT', 'PATCH']:
            request_data = request.POST or request.data  # Use POST data for form submissions or data for JSON payloads

        # Check parameters in the request data
        missing_parameters = [param for param in required_parameters if not request_data.get(param)]

        if missing_parameters:
            error_message = f'Missing or empty value for the parameter(s): {", ".join(missing_parameters)}'
            response_data = {'error': error_message}
            return generic_api_response(False, None, 400, response_data)

        # Continue with the request if all required parameters are present
        response = self.get_response(request)
        return response
