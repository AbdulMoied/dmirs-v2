from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    multipart_chunk_size = 15728640
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False