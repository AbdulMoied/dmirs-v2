from django.db import models


class DataTable(models.Model):
    table_name = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        db_table = 'tblLIBDataTable'


class DataTableColumns(models.Model):
    column_name = models.CharField(max_length=250, null=False, blank=False)
    alias = models.CharField(max_length=250, null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)
    data_table = models.ForeignKey(DataTable, on_delete=models.CASCADE, related_name='columns')

    class Meta:
        db_table = 'tblLIBDataTableColumn'
