from django.core.management.base import BaseCommand
import pandas as pd
import os

from dmirs.models import DataFile


class Command(BaseCommand):
    def handle(self, *args, **options):
        # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
        # Check if MetaHeader table has any records
        if DataFile.objects.exists():
            # If records exist, delete them
            self.stdout.write(self.style.SUCCESS('Deleting existing DataFile Names and codes...'))
            DataFile.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing DataFile Names and codes records deleted.'))

        # read the csv file into a dataframe
        df = pd.read_csv(os.path.abspath('dmirs/seed_files/gv_datafile_codes.csv'))
        print(df)
        # create a list of meta headers objects
        datafile_headers_list = []
        for index, row in df.iterrows():
            datafile_headers_list.append(
                DataFile(header_code=row['HeaderNo'], file_name=row['file_name'],
                         default_table=row['default_table'], default_view=row['default_view']))

        # bulk create the metaheaders objects
        DataFile.objects.bulk_create(datafile_headers_list)

        return 'Bulk create of DataFile Names and codes completed'
