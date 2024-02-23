import logging
import pandas as pd
import os
from django.db import connections
from dmirs.models import DataFileColumn

logger = logging.getLogger(__name__)


def generate_datafile_columns(client, db_identifier):
    # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
    # Check if MetaHeader table has any records
    if DataFileColumn.objects.filter(client=client).exists():
        # If records exist, delete them
        logger.info('Deleting existing DataFile Default Columns ')
        client_datafile_columns = DataFileColumn.objects.filter(client=client)
        client_datafile_columns.delete()
        logger.info('Existing DataFile Default Columns deleted.')

    # read the csv file into a dataframe
    df_excluded_columns = pd.read_csv(os.path.abspath('dmirs/config_files/excluded_columns.csv'), header=None)
    datafiles = client.datafile_set.all()

    # Create a list to store DataFileColumn objects
    datafile_columns_list = []

    for datafile in datafiles:
        connection = connections['db-mds']
        # Use the selected database
        connection.settings_dict['NAME'] = db_identifier
        with connection.cursor() as cursor:
            # Fetch the columns for the current data file
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{datafile.table}';")
            result = cursor.fetchall()
            columns = [row[0] for row in result]

            # Remove excluded columns
            columns_to_keep = [col for col in columns if col not in df_excluded_columns.iloc[0].tolist()]
            for order, column_name in enumerate(columns_to_keep, start=1):
                datafile_columns_list.append(
                    DataFileColumn(
                        column_name=column_name,
                        alias=column_name,
                        order=order,
                        data_file=datafile,
                        client=client
                    )
                )

        # Close the database connection after processing each data file
        connection.close()
    # Bulk create DataFileColumn objects
    DataFileColumn.objects.bulk_create(datafile_columns_list)
    return 'create of DataFile Default Columns completed'
