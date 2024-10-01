# Generated by Django 5.1.1 on 2024-10-01 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodFinder', '0008_userprofile_favorite_restaurants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='guest',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]