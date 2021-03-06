# Generated by Django 2.2.4 on 2019-11-23 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskAdvance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentary', models.TextField(max_length=2048)),
                ('task_file', models.FileField(upload_to='task_documents', verbose_name='file')),
                ('percentage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('comentary', models.CharField(blank=True, max_length=500, null=True)),
                ('sub_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.SubProgram')),
            ],
        ),
    ]
