# Generated by Django 4.2 on 2023-05-12 18:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_song_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='date',
            field=models.TextField(default=datetime.datetime(2023, 5, 12, 20, 31, 5, 429967)),
        ),
    ]