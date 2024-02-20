from django.db import connections, transaction
from rest_framework import status
from rest_framework.views import APIView
from backend_main.utils import generic_api_response

from dmirs.models import Client

from dmirs.utils.generate_headers import generate_headers
from dmirs.utils.generate_data_files import generate_data_files
from dmirs.utils.generate_datafile_columns import generate_datafile_columns


class ConfigView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        db_identifier = request.data.get('db_identifier')

        # Check if the database with the specific ID exists
        exists, error_message = self.check_database_exists(db_identifier)

        if not exists:
            return generic_api_response(False, errors=error_message, status=status.HTTP_404_NOT_FOUND)
        # Create a ClientDB record for the provided db_identifier in an atomic transaction
        with transaction.atomic():
            if not Client.objects.filter(db_id=db_identifier).exists():
                client = Client.objects.create(db_id=db_identifier)
                generate_data_files(client)
                generate_headers(client)
                generate_datafile_columns(client)
                print("Data Files successfully created")
                return generic_api_response(True, data={"message": "Success"},
                                            status=status.HTTP_200_OK)
            else:
                return generic_api_response(True, data={"message": "identifier already exists"},
                                            status=status.HTTP_200_OK)

    def check_database_exists(self, db_identifier):
        # Obtain the database connection from Django's ORM
        connection = connections['db-mds']

        # Check if the database with the specific ID exists in master.sys.databases
        with connection.cursor() as cursor:
            # Raw SQL query to check if the database exists
            query = f"SELECT 1 FROM master.sys.databases WHERE database_id = {db_identifier}"
            cursor.execute(query)
            exists = cursor.fetchone()

        if not exists:
            return False, f"Database with ID '{db_identifier}' does not exist."

        return True, None
