# Generated by Django 5.1.3 on 2025-01-06 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_remove_membroequipe_areas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membroequipe',
            name='photo',
            field=models.BinaryField(default=b''),
        ),
    ]
