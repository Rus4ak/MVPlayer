# Generated by Django 4.2 on 2023-05-22 12:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0027_remove_like_song_like_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='like',
            field=models.ManyToManyField(default=0, related_name='like_song', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
