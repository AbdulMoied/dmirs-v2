from dmirs.models import DataFileHeader, MetaHeader
import logging

logger = logging.getLogger(__name__)


def generate_datafile_headers(client):
    # Check if DataFileHeader table has any records for the specified client
    if DataFileHeader.objects.filter(client=client).exists():
        # If records exist, delete them
        logger.info('Deleting existing DataFile Default Headers ')
        client_datafile_headers = DataFileHeader.objects.filter(client=client)
        client_datafile_headers.delete()
        logger.info('Existing DataFile Default Headers deleted.')

    # Get all MetaHeader instances
    meta_headers = MetaHeader.objects.all()

    # Get all DataFile instances for the specified client
    data_files = client.datafile_set.all()

    # Create a list to store DataFileHeader instances
    data_file_headers = []

    # Iterate over each combination and create DataFileHeader instances
    for data_file in data_files:
        for order, meta_header in enumerate(meta_headers, start=1):
            # Create DataFileHeader instance and append to the list
            data_file_header = DataFileHeader(
                header=meta_header,
                order=order,
                data_file=data_file,
                client=client,
            )
            data_file_headers.append(data_file_header)

    # Use bulk_create to efficiently insert all instances at once
    DataFileHeader.objects.bulk_create(data_file_headers)
    return 'Bulk create of DataFile Default Headers completed'
