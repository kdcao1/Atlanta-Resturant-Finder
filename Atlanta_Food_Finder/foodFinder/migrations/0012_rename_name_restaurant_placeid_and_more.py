# Generated by Django 5.1.1 on 2024-10-01 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodFinder', '0011_rename_username_guest_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='name',
            new_name='placeId',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='address',
        ),
    ]
