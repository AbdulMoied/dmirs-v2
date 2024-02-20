from django.core.management.base import BaseCommand
import pandas as pd
import os

from dmirs.models import DatabaseObject


class Command(BaseCommand):
    def handle(self, *args, **options):
        # this function bulk creates records in the metaheaders table, from rows in the gv_headers.csv file
        # Check if MetaHeader table has any records
        if DatabaseObject.objects.exists():
            # If records exist, delete them
            self.stdout.write(self.style.SUCCESS('Deleting existing DataFile Names and codes...'))
            DatabaseObject.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing DataFile Names and codes records deleted.'))

        # read the csv file into a dataframe
        df = pd.read_csv(os.path.abspath('dmirs/config_files/column_mapping.csv'))
        print(df)
        # create a list of meta headers objects
        default_column_list = []
        for index, row in df.iterrows():
            default_column_list.append(
                DatabaseObject(name=row['Name'], default_columns=row['DefaultColumns']))

        # bulk create the metaheaders objects
        DatabaseObject.objects.bulk_create(default_column_list)

        return 'Bulk create of DataFile Names and codes completed'
