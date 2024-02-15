from django.core.management.base import BaseCommand
import pandas as pd
import os

from dmirs.models import MetaHeader


class Command(BaseCommand):
    def handle(self, *args, **options):
        # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
        # Check if MetaHeader table has any records
        if MetaHeader.objects.exists():
            # If records exist, delete them
            self.stdout.write(self.style.SUCCESS('Deleting existing MetaHeader records...'))
            MetaHeader.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing MetaHeader records deleted.'))

        # read the csv file into a dataframe
        df = pd.read_csv(os.path.abspath('dmirs/gv_headers.csv'))
        # create a list of meta headers objects
        metaheaders_list = []
        for index, row in df.iterrows():
            metaheaders_list.append(
                MetaHeader(header_code=row['HeaderNo'], description=row['Description'], default_value=row['default'],
                           sql_code=row['sqlcode']))

        # bulk create the metaheaders objects
        MetaHeader.objects.bulk_create(metaheaders_list)

        return 'Bulk create of meta headers complete'
