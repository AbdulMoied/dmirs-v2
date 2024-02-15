from django.db import models


class DataFile(models.Model):
    header_code = models.CharField(max_length=250, null=False, blank=False)
    default_table = models.CharField(max_length=250, null=True, blank=True)
    file_name = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        db_table = 'tblLIBReportType'
