from django.db import connections, transaction
from rest_framework import status
from rest_framework.views import APIView
from backend_main.utils import generic_api_response
from dmirs.models import Client
from dmirs.utils.generate_headers import generate_headers
from dmirs.utils.generate_data_files import generate_data_files
from dmirs.utils.generate_datafile_columns import generate_datafile_columns
from dmirs.models import MetaHeader

from dmirs.utils.generate_datafile_headers import generate_datafile_headers


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
                # all available meta Headers
                generate_headers(client)
                # default data files
                generate_data_files(client, db_identifier)
                # default data files columns
                generate_datafile_columns(client, db_identifier)
                generate_datafile_headers(client)
                print("Data Files successfully created")
                return generic_api_response(True, data={"message": "Success"},
                                            status=status.HTTP_200_OK)
            else:
                return generic_api_response(True, data={"message": "identifier already exists"},
                                            status=status.HTTP_200_OK)

    def check_database_exists(self, db_identifier):
        # Obtain the database connection from Django's ORM
        connection = connections['db-mds']

        # Check if the database with the specific name exists in master.sys.databases
        with connection.cursor() as cursor:
            # Raw SQL query to check if the database exists by name
            query = f"SELECT 1 FROM master.sys.databases WHERE name = '{db_identifier}'"
            cursor.execute(query)
            exists = cursor.fetchone()
        connection.close()
        if not exists:
            return False, f"Database with name '{db_identifier}' does not exist."

        return True, None


def test_function(request):
    db_identifier = request.GET.get('db_identifier')
    datafiles = MetaHeader.objects.all()
    print(datafiles)
    return generic_api_response(True, data={"message": "identifier already exists"}, )
