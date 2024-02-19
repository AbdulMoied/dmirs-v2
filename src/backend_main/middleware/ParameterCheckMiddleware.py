# middleware.py
from django.http import JsonResponse
from backend_main.utils import generic_api_response


class ParameterCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for required parameters in the request
        required_parameters = ['db_identifier']

        for param in required_parameters:
            param_value = request.GET.get(param)
            if param_value is None or param_value == '':
                response_data = {'error': f'Missing or empty value for the parameter: {param}'}
                return generic_api_response(False, None, 400, response_data)

        # Continue with the request if all required parameters are present
        response = self.get_response(request)
        return response
