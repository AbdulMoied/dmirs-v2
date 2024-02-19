from django.db import connections
from rest_framework import status

from rest_framework.views import APIView
from backend_main.utils import generic_api_response


# Import database module and define connection function
# ...

class TenementView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # Obtain the database connection from Django's ORM
        connection = connections['db-mds']
        # Use the selected database
        connection.settings_dict['NAME'] = request.GET.get('db_identifier')
        # Query your table in the selected database
        with connection.cursor() as cursor:
            cursor.execute("""SELECT [Lease_ID] FROM tblLeases""")
            tenements = [row[0] for row in cursor]

        # Convert to JSON serializable format
        serialized_tenements = [{'name': tenement} for tenement in tenements]
        return generic_api_response(True, serialized_tenements, status.HTTP_200_OK)
