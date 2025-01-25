# Generated by Django 5.1.4 on 2024-12-22 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
                ('brand', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('observation', models.TextField(blank=True, max_length=300, null=True)),
                ('location', models.CharField(max_length=100)),
                ('being_used', models.BooleanField(default=False)),
            ],
        ),
    ]
