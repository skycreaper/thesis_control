# Generated by Django 2.2.1 on 2019-05-28 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choice',
            new_name='Advance',
        ),
        migrations.RenameField(
            model_name='thesis',
            old_name='advance',
            new_name='porcentage',
        ),
    ]