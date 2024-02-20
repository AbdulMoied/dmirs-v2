import logging

from django.core.management.base import BaseCommand
import pandas as pd
import os

from dmirs.models import DataFile

logger = logging.getLogger(__name__)


def generate_data_file(client):
    # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
    # Check if MetaHeader table has any records
    if DataFile.objects.exists():
        # If records exist, delete them
        logger.info('Deleting existing DataFile Names and codes...')

        DataFile.objects.all().delete()
        logger.info('Existing DataFile Names and codes records deleted.')

    # read the csv file into a dataframe
    df = pd.read_csv(os.path.abspath('dmirs/config_files/gv_datafile_codes.csv'))

    # create a list of meta headers objects
    datafile_headers_list = []
    for index, row in df.iterrows():
        datafile_headers_list.append(
            DataFile(header_code=row['HeaderNo'], file_name=row['file_name'],
                     default_table=row['default_table'], default_view=row['default_view'], client=client))

    # bulk create the meta headers objects
    DataFile.objects.bulk_create(datafile_headers_list)

    return 'Bulk create of DataFile Names and codes completed'
