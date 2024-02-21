from django.db import connections
from django.db import connections


def get_database_name(db_identifier):
    # Obtain the database connection from Django's ORM
    connection = connections['db-mds']

    # Check if the database with the specific ID exists in master.sys.databases
    with connection.cursor() as cursor:
        # Raw SQL query to check if the database exists
        query = f"SELECT name FROM master.sys.databases WHERE database_id = {db_identifier}"
        cursor.execute(query)
        result = cursor.fetchone()

    # Extract the database name from the result or return an empty string
    db_name = result[0] if result else ""

    return db_name
