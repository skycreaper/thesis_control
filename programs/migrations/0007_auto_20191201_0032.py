# Generated by Django 2.2.4 on 2019-12-01 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0006_taskadvance_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskadvance',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
