from django.db import connections
from rest_framework import status

from rest_framework.views import APIView
from backend_main.utils import generic_api_response

from dmirs.models import Client


# Import database module and define connection function
# ...

class TenementView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        db_identifier = request.GET.get('db_identifier')

        # Check if the ClientDB record exists
        if not Client.objects.filter(db_id=db_identifier).exists():
            data = {
                "message": "Configuration not found.",
                "details": "Automated configuration is required. Please trigger the configuration endpoint to set up "
                           "your environment."
            }
            return generic_api_response(False, None, 404, errors=data)

        # Obtain the database connection from Django's ORM
        connection = connections['db-mds']
        # Use the selected database
        connection.settings_dict['NAME'] = db_identifier
        # Query your table in the selected database
        with connection.cursor() as cursor:
            cursor.execute("""SELECT [Lease_ID] FROM tblLeases""")
            tenements = [row[0] for row in cursor]

        # Convert to JSON serializable format
        serialized_tenements = [{'name': tenement} for tenement in tenements]
        return generic_api_response(True, serialized_tenements, status.HTTP_200_OK)
