from django.db import models
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#6c757d")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class SystemConfig(models.Model):
    CONFIG_KEYS = [
        ("env_data_sources",    "Ortamda Bulunan Veri Kaynakları (virgülle)"),
        ("env_os_types",        "Ortamda Bulunan OS Tipleri (virgülle)"),
        ("env_mitre_focus",     "Öncelikli MITRE Tactic'ler (virgülle)"),
        ("similarity_threshold","Benzer Kural Eşiği (0-100, varsayılan 70)"),
        ("default_analyst",     "Varsayılan Atanan Analist"),
        ("export_columns_escu", "CSV Export'a Dahil Edilecek ESCU Kolonlar"),
        ("export_columns_cb",   "CSV Export'a Dahil Edilecek CB Kolonlar"),
        ("review_sla_days",     "İnceleme SLA Günü (varsayılan 14)"),
    ]
    key = models.CharField(max_length=100, unique=True, choices=CONFIG_KEYS)
    value = models.TextField(blank=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    @classmethod
    def get(cls, key, default=""):
        try: return cls.objects.get(key=key).value
        except cls.DoesNotExist: return default
    def __str__(self): return self.key

class AuditLog(models.Model):
    ACTION_CHOICES = [("create", "Create"), ("update", "Update"), ("delete", "Delete"), ("import", "Import"), ("assign", "Assign"), ("stage_change", "Stage Change"), ("convert", "Convert"), ("export", "Export")]
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=100)
    entity_id = models.IntegerField()
    entity_label = models.CharField(max_length=255)
    actor_name = models.CharField(max_length=150, default="system")
    detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
