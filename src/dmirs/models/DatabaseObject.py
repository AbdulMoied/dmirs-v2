from django.db import models


class DatabaseObject(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, unique=True)
    default_columns = models.TextField(null=False, blank=True)

    class Meta:
        db_table = 'tblLIBDefaultColumn'
