import os
import zipfile
import io
from datetime import datetime
import pandas as pd
from django.db import connections
from django.http import FileResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from backend_main.utils import generic_api_response
from dmirs.forms import DataForm

from dmirs.utils.get_qualified_holes import get_qualified_holes
from dmirs.utils.get_qualified_collar_files import get_qualified_collar_files
from dmirs.utils.get_client import get_client


class QualifiedDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        form = DataForm(request.GET)
        db_identifier = request.GET.get('db_identifier')

        if form.is_valid():
            qualified_Holes = get_qualified_holes(form.cleaned_data['start_date'], form.cleaned_data['end_date'],
                                                  form.cleaned_data['tenements'], db_identifier)
            # Get Client
            client = get_client(db_identifier)
            # Get Data File is type Collar
            datafiles_for_client = client.datafile_set.filter(type='collar')
            # Gethar the holeids for query
            placeholders = ', '.join(['%s'] * len(qualified_Holes))
            # Get qualified collar types
            qualified_collar_files = get_qualified_collar_files(qualified_Holes, db_identifier, datafiles_for_client)
            zip_buffer = io.BytesIO()

            try:
                with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
                    for datafile in qualified_collar_files:
                        print("processing " + datafile.table)
                        # Access file columns
                        datafile_columns = datafile.columns.all()
                        # Get a list of column names
                        column_names = [column.column_name for column in datafile_columns]
                        # Query to fetch data based on columns
                        data_query = f"""SELECT {', '.join(column_names)} FROM "{datafile.table}" WHERE hole_id IN ({placeholders})"""

                        try:
                            conn = connections['db-mds']
                            # Use the selected database
                            conn.settings_dict['NAME'] = db_identifier
                            # Use parameterized query
                            df = pd.read_sql(data_query, conn, params=qualified_Holes)
                            file_name = datafile.file_name + '.txt'
                            folder_name = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(
                                datetime.now().day)
                            file_buffer = io.StringIO()
                            # Add 'D' in front of every row with a tab
                            df['D'] = 'D'  # Add 'D' prefix to each row
                            df = df[['D'] + column_names]  # Reorder columns, placing 'D' at the beginning
                            df.to_csv(file_buffer, sep='\t', mode='a', index=False, header=False)
                            file_buffer.seek(0)
                            zip_file.writestr(folder_name + '/' + file_name,
                                              file_buffer.getvalue())
                        except Exception as e:
                            # Log the error
                            print(f"Error processing {datafile.table}: {e}")
                        finally:
                            # Close the connection explicitly
                            conn.close()

            except Exception as zip_error:
                # Log the error
                print(f"Error creating ZIP file: {zip_error}")

            zip_buffer.seek(0)
            return FileResponse(zip_buffer, as_attachment=True, filename='digi-data.zip')
        else:
            return generic_api_response(False, None, status.HTTP_400_BAD_REQUEST, form.errors)

    def insert_data_header(self, client):
        return
