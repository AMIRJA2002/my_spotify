# Generated by Django 4.2 on 2023-04-18 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_rename_dateadded_addsonganddateadded'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]