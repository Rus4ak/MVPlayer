# Generated by Django 4.2 on 2023-05-12 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_song_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 18, 38, 58, 252948, tzinfo=datetime.timezone.utc)),
        ),
    ]
