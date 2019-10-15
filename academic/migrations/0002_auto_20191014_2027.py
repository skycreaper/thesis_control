# Generated by Django 2.2.4 on 2019-10-15 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='institutional_information',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='academic.InstitutionalInformation'),
        ),
        migrations.AddField(
            model_name='student',
            name='personal_information',
            field=models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, to='academic.PersonalInformation'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='civil_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.CivilState'),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Gender'),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='health_information',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='academic.HealthInformation'),
        ),
        migrations.AddField(
            model_name='personalinformation',
            name='nationality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Nationality'),
        ),
        migrations.AddField(
            model_name='comentsthread',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Teacher'),
        ),
        migrations.AddField(
            model_name='advance',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Thesis'),
        ),
    ]
