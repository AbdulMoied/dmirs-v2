# Generated by Django 4.2.3 on 2024-02-16 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmirs', '0003_alter_datafile_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatabaseObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('default_columns', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'tblLIBDefaultColumn',
            },
        ),
        migrations.CreateModel(
            name='DataTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'tblLIBDataTable',
            },
        ),
        migrations.AddField(
            model_name='datafile',
            name='default_view',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='DataTableColumns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=250)),
                ('alias', models.CharField(max_length=250)),
                ('order', models.IntegerField()),
                ('data_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='dmirs.datatable')),
            ],
            options={
                'db_table': 'tblLIBDataTableColumn',
            },
        ),
    ]
