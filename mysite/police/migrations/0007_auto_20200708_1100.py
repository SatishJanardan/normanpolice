# Generated by Django 3.0.7 on 2020-07-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0006_weather'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='wPressureMax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wPressureMin',
            field=models.FloatField(),
        ),
    ]
