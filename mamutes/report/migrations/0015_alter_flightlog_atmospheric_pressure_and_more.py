# Generated by Django 5.1.4 on 2025-02-08 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0014_alter_accidentlog_id_flightlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightlog',
            name='atmospheric_pressure',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
        migrations.AlterField(
            model_name='flightlog',
            name='total_takeoff_weight',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='flightlog',
            name='wind_speed',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
    ]
