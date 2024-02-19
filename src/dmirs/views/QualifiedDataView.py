from django.db import connections
from rest_framework import status

from rest_framework.views import APIView
from backend_main.utils import generic_api_response

from dmirs.forms import DataForm


# Import database module and define connection function
# ...

class QualifiedDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        form = DataForm(request.GET)

        # Check if the form is valid
        if form.is_valid():

            return generic_api_response(True, form.cleaned_data['tenements'], status.HTTP_200_OK)
        else:
            # Form is not valid, return an error response
            return generic_api_response(False, None, status.HTTP_400_BAD_REQUEST, form.errors)
