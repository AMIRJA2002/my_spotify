# Generated by Django 4.2 on 2023-04-14 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='like_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='music',
            name='like_count',
            field=models.BigIntegerField(default=0),
        ),
    ]