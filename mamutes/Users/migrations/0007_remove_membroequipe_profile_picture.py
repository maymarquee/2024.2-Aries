# Generated by Django 5.1.4 on 2024-12-16 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_membroequipe_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membroequipe',
            name='profile_picture',
        ),
    ]
