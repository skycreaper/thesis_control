# Generated by Django 2.2.4 on 2019-10-15 01:57

from django.db import migrations



class Migration(migrations.Migration):

    def pupulate_gender(apps, schema_editor):
        Gender = apps.get_model('academic', 'Gender')
        Gender.objects.bulk_create([
            Gender(name="Masculino", description="Masculino"),
            Gender(name="Femenino", description="Femenino"),
        ])

    def pupulate_civil_state(apps, schema_editor):
        civil_state = apps.get_model('academic', 'CivilState')
        civil_state.objects.bulk_create([
            civil_state(name= "Soltero/a", description="Soltero/a"),
            civil_state(name= "Casado/a", description="Casado/a"),
            civil_state(name= "Viudo/a", description="Viudo/a"),
            civil_state(name= "Unión libre", description="Unión libre"),
            civil_state(name= "Divorciado/a", description="Divorciado/a"),
        ])

    def populate_nationality(apps, schema_editor):
        Nationality = apps.get_model('academic', 'Nationality')
        Nationality.objects.bulk_create([
            Nationality(name= "Colombia", description="Colombiano/a", origin_country="Colombia"),
            Nationality(name= "México", description="Méxicano/a", origin_country="México"),
            Nationality(name= "Brasil", description="Brasileño/a", origin_country="Brasil"),
            Nationality(name= "Estados Unidos", description="Estadounidénse", origin_country="Estados Unidos"),
            Nationality(name= "Reino Unido", description="Británico/a", origin_country="Reino Unido"),
        ])

    def populate_investigation_line(apps, schema_editor):
        InvestigationLine = apps.get_model('academic', 'InvestigationLine')
        InvestigationLine.objects.bulk_create([
            InvestigationLine(name= "Categoría 1", description="Categoría 1"),
            InvestigationLine(name= "Categoría 2", description="Categoría 2"),
            InvestigationLine(name= "Categoría 3", description="Categoría 3"),
        ])

    dependencies = [
        ('academic', '0002_auto_20191014_2027'),
    ]

    operations = [
        migrations.RunPython(pupulate_gender),
        migrations.RunPython(pupulate_civil_state),
        migrations.RunPython(populate_nationality),
        migrations.RunPython(populate_investigation_line),
    ]
