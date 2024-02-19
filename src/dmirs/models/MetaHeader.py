from django.db import models
from .ClientDB import ClientDB


class MetaHeader(models.Model):
    header_code = models.CharField(primary_key=True, max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    default_value = models.CharField(max_length=250, default=None, null=False, blank=False)
    sql_code = models.CharField(max_length=250, default=None, null=False, blank=False)
    client = models.ForeignKey(ClientDB, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblHeader'
