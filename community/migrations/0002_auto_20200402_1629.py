# Generated by Django 3.0.4 on 2020-04-02 16:29

import common.storage
import community.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='icon',
            field=models.ImageField(default='community/default_icon.png', storage=common.storage.OverwriteStorage(), upload_to=community.models.CommunityIconSavePath),
        ),
    ]
