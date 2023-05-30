# Generated by Django 4.2 on 2023-05-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_song_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='genre',
            field=models.CharField(default='genre', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='song',
            name='listening',
            field=models.IntegerField(default=0),
        ),
    ]
