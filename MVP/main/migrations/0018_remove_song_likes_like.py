# Generated by Django 4.2 on 2023-05-17 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_genre_alter_song_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='likes',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.song')),
            ],
        ),
    ]
