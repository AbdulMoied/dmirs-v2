from django.db import models


class Report(models.Model):
    header_code = models.CharField(max_length=250, null=False, blank=False)
    default_table = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        db_table = 'tblLIBReport'
