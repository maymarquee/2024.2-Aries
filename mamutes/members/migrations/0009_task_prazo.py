# Generated by Django 5.1.3 on 2024-12-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_alter_task_completion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='Prazo',
            field=models.DateField(blank=True, null=True),
        ),
    ]
