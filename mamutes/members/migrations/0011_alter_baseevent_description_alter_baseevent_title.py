# Generated by Django 5.1 on 2025-01-14 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_remove_event_description_remove_event_is_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseevent',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='baseevent',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
