# Generated by Django 2.2.4 on 2019-09-28 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0015_auto_20190927_2005'),
    ]

    def populate_rol(apps, schema_editor):
        Rol = apps.get_model('academic', 'Rol')
        Rol.objects.bulk_create([
            Rol(name= "Profesor", description="Profesor a tiempo completo"),
            Rol(name= "Estudiante", description="Estudiante de pregrado"),
            Rol(name= "Administrador", description="Administrador del sistema"),
        ])

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='institutionalinformation',
            name='rol',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='academic.Rol'),
            preserve_default=False,
        ),
        migrations.RunPython(populate_rol),
    ]
