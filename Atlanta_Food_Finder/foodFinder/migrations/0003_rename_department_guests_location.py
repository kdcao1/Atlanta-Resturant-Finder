# Generated by Django 5.1.1 on 2024-09-14 23:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodFinder', '0002_rename_employee_guests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guests',
            old_name='department',
            new_name='location',
        ),
    ]
