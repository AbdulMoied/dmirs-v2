from django.db import models
from .MetaHeader import MetaHeader
from .Client import Client


class DataFile(models.Model):
    header_code = models.CharField(max_length=250, null=False, blank=False)
    default_table = models.CharField(max_length=250, null=True, blank=True)
    default_view = models.CharField(max_length=250, null=True, blank=True)
    file_name = models.CharField(max_length=250, null=False, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblDatafile'
        unique_together = ('header_code', 'client')


class DataFileHeader(models.Model):
    header = models.ForeignKey(MetaHeader, on_delete=models.CASCADE)
    order = models.IntegerField()
    data_file = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblDatafileHeader'
        unique_together = ('data_file', 'header', 'client')


class DataFileColumns(models.Model):
    column_name = models.CharField(max_length=250, null=False, blank=False)
    alias = models.CharField(max_length=250, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)
    data_file = models.ForeignKey(DataFile, on_delete=models.CASCADE, related_name='columns')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tblDatafileColumn'
        unique_together = ('column_name', 'data_file', 'client')
