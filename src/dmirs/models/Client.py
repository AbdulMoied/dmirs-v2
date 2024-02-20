from django.db import models


class Client(models.Model):
    db_id = models.CharField(max_length=250, unique=True, null=False, blank=False)
    name = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'tblClient'
