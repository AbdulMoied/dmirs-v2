from django.db import connections
from .get_database_name import get_database_name


def get_qualified_holes(start_date, end_date, tenements, db_identifier):
    connection = connections['db-mds']
    # Use the selected database
    connection.settings_dict['NAME'] = db_identifier  # get_database_name(db_identifier)
    # Query your table in the selected database
    with connection.cursor() as cursor:
        # Create a string of placeholders based on the number of tenements
        placeholders = ', '.join(['%s'] * len(tenements))

        query = f"""
                            SELECT [Hole_ID] 
                            FROM tblDHColl 
                            WHERE Lease_ID IN ({placeholders})
                            AND Date_Started BETWEEN %s AND %s
                        """.format(placeholders=placeholders)
        params = tenements + [start_date, end_date]
        cursor.execute(query, params)
        Hole_ids = [row[0] for row in cursor.fetchall()]
        return Hole_ids
