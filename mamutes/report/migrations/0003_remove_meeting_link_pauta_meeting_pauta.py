# Generated by Django 5.1.4 on 2025-02-03 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='link_pauta',
        ),
        migrations.AddField(
            model_name='meeting',
            name='pauta',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
