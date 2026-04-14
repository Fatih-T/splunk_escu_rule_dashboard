from django.db import models
from apps.escu.models import PIPELINE_STAGES

class CBRule(models.Model):
    name = models.CharField(max_length=500)
    rule_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    query = models.TextField(blank=True)
    severity = models.CharField(max_length=50, blank=True)
    mitre_tactic = models.CharField(max_length=255, blank=True)
    mitre_technique = models.CharField(max_length=255, blank=True)
    mitre_technique_id = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=PIPELINE_STAGES, default="new")
    not_applicable_reason = models.TextField(blank=True)
    tags = models.ManyToManyField("core.Tag", blank=True)
    assigned_analyst = models.CharField(max_length=150, blank=True)
    source_escu_rule = models.ForeignKey("escu.ESCURule", on_delete=models.SET_NULL, null=True, blank=True, related_name="cb_conversions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["name"]
    def __str__(self): return self.name
    def get_status_badge(self):
        BADGE_MAP = {"new": "secondary", "under_review": "info", "not_applicable": "dark", "applicable": "primary", "in_progress": "warning", "ready_for_cb": "light", "converted": "success", "active": "success", "tuning": "warning", "deprecated": "danger"}
        return BADGE_MAP.get(self.status, "secondary")
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = CBRule.objects.get(pk=self.pk)
                CBRuleVersion.objects.create(rule=old, snapshot={"name": old.name, "query": old.query, "status": old.status, "description": old.description}, changed_by="system", change_summary="Rule updated")
            except CBRule.DoesNotExist: pass
        super().save(*args, **kwargs)

class CBRuleVersion(models.Model):
    rule = models.ForeignKey(CBRule, on_delete=models.CASCADE, related_name="versions")
    snapshot = models.JSONField()
    changed_by = models.CharField(max_length=150, default="system")
    change_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.rule.name} v{self.created_at}"
