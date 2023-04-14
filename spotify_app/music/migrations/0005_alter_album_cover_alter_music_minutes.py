# Generated by Django 4.2 on 2023-04-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_alter_album_songs_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='album/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='minutes',
            field=models.FloatField(default=0),
        ),
    ]
