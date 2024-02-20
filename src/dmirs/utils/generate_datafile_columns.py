import logging
import pandas as pd
import os

from django.db.models import Q
from dmirs.models import DataFileColumns

from dmirs.models import DataFile

logger = logging.getLogger(__name__)


def generate_datafile_columns(client):
    # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
    # Check if MetaHeader table has any records
    if DataFileColumns.objects.exists():
        # If records exist, delete them
        logger.info('Deleting existing DataFile Default Columns ')
        client_datafile_columns = DataFileColumns.objects.filter(client=client)
        client_datafile_columns.delete()
        logger.info('Existing DataFile Default Columns deleted.')

    # read the csv file into a dataframe
    df = pd.read_csv(os.path.abspath('dmirs/config_files/column_mapping.csv'))
    # Iterate over rows in the DataFrame
    for index, row in df.iterrows():
        # Check if 'Name' exists in either 'default_table' or 'default_view'
        data_file = DataFile.objects.filter(Q(default_table=row['Name']) | Q(default_view=row['Name'])).first()
        if data_file:
            # Iterate over default_columns and create DataFileColumns records
            for order, column_name in enumerate(row['DefaultColumns'].split(','), start=1):
                DataFileColumns.objects.create(
                    column_name=column_name.strip(),
                    alias=column_name.strip(),  # You may adjust this as needed
                    order=order,
                    data_file=data_file,
                    client=client
                )

    return 'create of DataFile Default Columns completed'
