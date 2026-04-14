from django.db import migrations
def create_data(apps, schema_editor):
    SC = apps.get_model('core', 'SystemConfig')
    configs = [
        ("env_data_sources", "Sysmon, WinEventLog, O365, AWS CloudTrail", "Ortamda Bulunan Veri Kaynakları"),
        ("env_os_types", "Windows, Linux, macOS", "Ortamda Bulunan OS Tipleri"),
        ("env_mitre_focus", "Persistence, Privilege Escalation, Defense Evasion", "Öncelikli MITRE Tactic'ler"),
        ("similarity_threshold", "70", "Benzer Kural Eşiği (0-100)"),
        ("default_analyst", "analyst_1", "Varsayılan Atanan Analist"),
        ("export_columns_escu", "rule_id,name,status,severity,mitre_tactic", "CSV Export'a Dahil Edilecek ESCU Kolonlar"),
        ("export_columns_cb", "rule_id,name,status,severity,mitre_tactic", "CSV Export'a Dahil Edilecek CB Kolonlar"),
        ("review_sla_days", "14", "İnceleme SLA Günü"),
    ]
    for key, value, desc in configs:
        SC.objects.get_or_create(key=key, defaults={"value": value, "description": desc})

class Migration(migrations.Migration):
    dependencies = [('core', '0002_initial_data')]
    operations = [migrations.RunPython(create_data)]
