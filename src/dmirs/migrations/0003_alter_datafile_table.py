# Generated by Django 4.2.3 on 2024-02-15 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dmirs', '0002_rename_report_datafile_rename_headers_metaheader_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='datafile',
            table='tblLIBReportType',
        ),
    ]
