# Generated by Django 5.1.3 on 2025-02-02 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_membroequipe_photo'),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('meeting_date', models.DateField()),
                ('meeting_time_begin', models.TimeField()),
                ('meeting_time_end', models.TimeField()),
                ('local', models.CharField(max_length=255)),
                ('is_remote', models.BooleanField(default=False)),
                ('link', models.URLField(blank=True)),
                ('other_participants', models.TextField(blank=True, null=True)),
                ('link_pauta', models.URLField(blank=True, null=True)),
                ('areas', models.ManyToManyField(to='Users.area')),
            ],
        ),
    ]
