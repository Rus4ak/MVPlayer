# Generated by Django 4.2 on 2023-05-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_playlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='song',
        ),
        migrations.AddField(
            model_name='like',
            name='song',
            field=models.ManyToManyField(to='main.song'),
        ),
    ]
