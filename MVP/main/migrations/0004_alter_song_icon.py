# Generated by Django 4.2 on 2023-05-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_song_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='icon',
            field=models.ImageField(upload_to='img/'),
        ),
    ]
