# Generated by Django 2.2.4 on 2019-12-17 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0011_auto_20191216_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subprogram',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='subprogramtask',
            name='commentary',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]