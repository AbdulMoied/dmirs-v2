from django.db import models

from .MetaHeader import MetaHeader


class DataFile(models.Model):
    header_code = models.CharField(max_length=250, null=False, blank=False)
    default_table = models.CharField(max_length=250, null=True, blank=True)
    default_view = models.CharField(max_length=250, null=True, blank=True)
    file_name = models.CharField(max_length=250, null=False, blank=False)
    headers = models.ManyToManyField('MetaHeader', through='DataFileHeader', related_name='tblDatafileHeader')

    class Meta:
        db_table = 'tblLIBReportType'


class DataFileHeader(models.Model):
    data_file = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    header = models.ForeignKey(MetaHeader, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        db_table = 'tblDatafileHeader'
        unique_together = ('data_file', 'header')
