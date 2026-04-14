from django.db import models

PIPELINE_STAGES = [
    ("new", "New"), ("under_review", "Under Review"),
    ("not_applicable", "Not Applicable"), ("applicable", "Applicable"),
    ("in_progress", "In Progress"), ("ready_for_cb", "Ready for CB"),
    ("converted", "Converted"), ("active", "Active"),
    ("tuning", "Tuning"), ("deprecated", "Deprecated"),
]

class ESCUImportBatch(models.Model):
    STATUS_CHOICES = [("pending","Pending"),("processed","Processed"),("failed","Failed")]
    filename = models.CharField(max_length=255)
    file_path = models.FileField(upload_to="uploads/escu/")
    imported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    rules_added = models.IntegerField(default=0)
    rules_updated = models.IntegerField(default=0)
    rules_deprecated = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    def __str__(self): return f"Batch #{self.pk} - {self.filename}"

class ESCURule(models.Model):
    name = models.CharField(max_length=500)
    rule_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    mitre_tactic = models.CharField(max_length=255, blank=True)
    mitre_technique = models.CharField(max_length=255, blank=True)
    mitre_technique_id = models.CharField(max_length=50, blank=True)
    severity = models.CharField(max_length=50, blank=True)
    search = models.TextField(blank=True)
    data_source = models.CharField(max_length=255, blank=True)
    how_to_implement = models.TextField(blank=True)
    known_false_positives = models.TextField(blank=True)
    raw_csv_row = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=PIPELINE_STAGES, default="new")
    not_applicable_reason = models.TextField(blank=True)
    tags = models.ManyToManyField("core.Tag", blank=True)
    assigned_analyst = models.CharField(max_length=150, blank=True)
    first_seen_batch = models.ForeignKey(ESCUImportBatch, on_delete=models.SET_NULL, null=True, related_name="new_rules")
    last_seen_batch = models.ForeignKey(ESCUImportBatch, on_delete=models.SET_NULL, null=True, related_name="seen_rules")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["name"]
    def __str__(self): return self.name
    def get_status_badge(self):
        return {"new": "secondary", "under_review": "info", "not_applicable": "dark", "applicable": "primary", "in_progress": "warning", "ready_for_cb": "light", "converted": "success", "active": "success", "tuning": "warning", "deprecated": "danger"}.get(self.status, "secondary")

class ESCURuleVersion(models.Model):
    rule = models.ForeignKey(ESCURule, on_delete=models.CASCADE, related_name="versions")
    batch = models.ForeignKey(ESCUImportBatch, on_delete=models.CASCADE)
    snapshot = models.JSONField()
    change_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.rule.name} v{self.created_at}"
