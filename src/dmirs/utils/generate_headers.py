import logging

import pandas as pd
import os

from dmirs.models import MetaHeader

logger = logging.getLogger(__name__)


def generate_headers(client):
    # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
    # Check if MetaHeader table has any records
    if MetaHeader.objects.exists():
        # If records exist, delete them
        logger.info('Deleting existing MetaHeader records...')
        client_meta_headers = MetaHeader.objects.filter(client=client)
        client_meta_headers.delete()
        logger.info('Existing MetaHeader records deleted.')

    # read the csv file into a dataframe
    df = pd.read_csv(os.path.abspath('dmirs/config_files/gv_headers.csv'))
    # create a list of meta headers objects
    meta_headers_list = []
    for index, row in df.iterrows():
        meta_headers_list.append(
            MetaHeader(header_code=row['HeaderNo'], description=row['Description'], default_value=row['default'],
                       sql_code=row['sqlcode'], client=client))

    # bulk create the meta headers objects
    MetaHeader.objects.bulk_create(meta_headers_list)
    logger.info('Bulk create of meta headers completed')
    return 'Bulk create of meta headers completed'
