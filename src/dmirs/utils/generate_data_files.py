import logging
import pandas as pd
import os

from django.db import connections
from dmirs.models import DataFile

logger = logging.getLogger(__name__)


def generate_data_files(client, db_identifier):
    # this function bulk creates records in the meta headers table, from rows in the gv_headers.csv file
    # Check if MetaHeader table has any records
    if DataFile.objects.filter(client=client).exists():
        # If records exist, delete them
        logger.info('Deleting existing DataFile Names and codes...')
        client_data_files = DataFile.objects.filter(client=client)
        client_data_files.delete()
        logger.info('Existing DataFile Names and codes records deleted.')

    # read the csv file into a dataframe
    df = pd.read_csv(os.path.abspath('dmirs/config_files/gv_datafile_codes.csv'))
    # create a list of meta headers objects
    datafile_list = []
    connection = connections['db-mds']
    # Use the selected database
    connection.settings_dict['NAME'] = db_identifier

    with connection.cursor() as cursor:
        try:
            # Get all views and tables
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS")
            views = {row[0] for row in cursor.fetchall()}  # Use a set for faster membership testing
        except Exception as e:
            print(str(e))
    connection.close()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.Tables")
            tables = {row[0] for row in cursor.fetchall()}
        except Exception as e:

            print(str(e))
    connection.close()
    # Combine the sets of tables and views
    all_tables_and_views = tables.union(views)

    for index, row in df.iterrows():
        table_name = row['table']

        if not pd.isna(table_name) and table_name in all_tables_and_views:
            print("view/table exists " + str(table_name))
            datafile_list.append(
                DataFile(header_code=row['HeaderNo'], file_name=row['file_name'],
                         table=table_name, type=row['type'], client=client))
        else:
            logger.warning(
                f"The specified table or table or view '{table_name}'  does not exist in database '{db_identifier}'. Skipping...")

    # bulk create the meta headers objects
    DataFile.objects.bulk_create(datafile_list)
    logger.info('Bulk create of DataFile completed')

    # Close the database connection after processing
    connection.close()
    return 'Bulk create of DataFile Names and codes completed'
