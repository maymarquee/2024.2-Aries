# Generated by Django 5.1.3 on 2025-01-14 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Baixa Prioridade'), (2, 'Média Prioridade'), (3, 'Alta Prioridade')]),
        ),
    ]
