from django.db import models
from .Client import Client


class MetaHeader(models.Model):
    header_code = models.CharField(max_length=250, null=False, blank=False)
    description = models.CharField(max_length=250, null=False, blank=False)
    default_value = models.CharField(max_length=250, default=None, null=False, blank=False)
    sql_code = models.CharField(max_length=250, default=None, null=False, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblHeader'
        unique_together = ('header_code', 'client')
