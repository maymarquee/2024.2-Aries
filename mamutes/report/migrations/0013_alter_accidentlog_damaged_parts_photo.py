# Generated by Django 5.1 on 2025-02-08 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0012_remove_accidentlog_pilot_flight_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accidentlog',
            name='damaged_parts_photo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
