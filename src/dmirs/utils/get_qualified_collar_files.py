from django.db import connections
from .get_database_name import get_database_name


def get_qualified_collar_files(hole_ids, db_name, datafiles):
    qualified_files = []
    connection = connections['db-mds']
    # Use the selected database
    connection.settings_dict['NAME'] = db_name
    # hole_ids = ', '.join(['%s'] * len(hole_ids))
    for datafile in datafiles:
        # Assuming datafile.table contains the table name
        table_name = datafile.table
        placeholders = ', '.join(['%s'] * len(hole_ids))
        # Assuming there is a column named 'hole_id' in the table
        query = f"""SELECT COUNT(hole_id) FROM {table_name} WHERE hole_id IN ({placeholders})"""

        # Execute the query with the list of hole_ids
        with connection.cursor() as cursor:
            cursor.execute(query, hole_ids)
            result = cursor.fetchone()
        # Check if any matching hole_ids were found
        if result and result[0] > 0:
            qualified_files.append(datafile)
            print(f"{datafile.table}: {result[0]} matching records")

    return qualified_files
