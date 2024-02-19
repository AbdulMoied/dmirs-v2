from django.db import models


class ClientDB(models.Model):
    db_id = models.CharField(max_length=250, unique=True, null=False, blank=False)
    name = models.CharField(max_length=250, unique=True, null=False, blank=False)

    class Meta:
        db_table = 'tblClient'
