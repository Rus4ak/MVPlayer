# Generated by Django 4.2 on 2023-05-19 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_playlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='user',
        ),
    ]