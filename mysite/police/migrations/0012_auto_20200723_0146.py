# Generated by Django 3.0.8 on 2020-07-23 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0011_graphdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graphdata',
            old_name='bucketSize',
            new_name='bucket_Size',
        ),
        migrations.RenameField(
            model_name='graphdata',
            old_name='endDate',
            new_name='end_Date',
        ),
        migrations.RenameField(
            model_name='graphdata',
            old_name='endUrg',
            new_name='end_Urgency',
        ),
        migrations.RenameField(
            model_name='graphdata',
            old_name='startDate',
            new_name='start_Date',
        ),
        migrations.RenameField(
            model_name='graphdata',
            old_name='startUrg',
            new_name='start_Urgency',
        ),
    ]
