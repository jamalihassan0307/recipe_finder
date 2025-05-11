from django.db import migrations

def create_default_role(apps, schema_editor):
    Role = apps.get_model('app', 'Role')
    Role.objects.create(role_name='admin')

def remove_default_role(apps, schema_editor):
    Role = apps.get_model('app', 'Role')
    Role.objects.filter(role_name='admin').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_role, remove_default_role),
    ] 