# Generated by Django 3.0.4 on 2020-04-02 14:19

import common.storage
import community.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('tagline', models.CharField(max_length=50)),
                ('about', models.CharField(max_length=500)),
                ('icon', models.ImageField(default='profile_pics/default.png', storage=common.storage.OverwriteStorage(), upload_to=community.models.CommunityIconSavePath)),
                ('banner', models.ImageField(blank=True, null=True, storage=common.storage.OverwriteStorage(), upload_to=community.models.CommunityBannerSavePath)),
                ('dt_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('admins', models.ManyToManyField(related_name='administered_communities', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_join', models.DateTimeField(default=django.utils.timezone.now)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.Community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='joined_communities', through='community.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
