from django.db import migrations
def create_data(apps, schema_editor):
    SC = apps.get_model('core', 'SystemConfig')
    SC.objects.create(key="default_analyst", value="analyst_1")
    SC.objects.create(key="similarity_threshold", value="70")
class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]
    operations = [migrations.RunPython(create_data)]
