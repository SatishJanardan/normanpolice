# Generated by Django 3.0.8 on 2020-07-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0012_auto_20200723_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='caseFiledate',
            field=models.DateField(default='2020-06-01'),
        ),
        migrations.AddField(
            model_name='crime',
            name='crimeCase',
            field=models.CharField(choices=[('N', 'No'), ('Y', 'Yes')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='graphdata',
            name='end_Date',
            field=models.DateTimeField(default='2020-07-09 12:00:00'),
        ),
    ]
