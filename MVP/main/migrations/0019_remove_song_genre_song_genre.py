# Generated by Django 4.2 on 2023-05-17 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_remove_song_likes_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='genre',
        ),
        migrations.AddField(
            model_name='song',
            name='genre',
            field=models.ManyToManyField(to='main.genre'),
        ),
    ]
