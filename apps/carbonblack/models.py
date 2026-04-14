from django.db import models
from apps.escu.models import PIPELINE_STAGES
class CBRule(models.Model):
    name = models.CharField(max_length=500)
    rule_id = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    query = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=PIPELINE_STAGES, default="new")
    assigned_analyst = models.CharField(max_length=150, blank=True)
    source_escu_rule = models.ForeignKey("escu.ESCURule", on_delete=models.SET_NULL, null=True, blank=True, related_name="cb_conversions")
    created_at = models.DateTimeField(auto_now_add=True)
    def get_status_badge(self):
        return {"new": "secondary", "active": "success"}.get(self.status, "secondary")
class CBRuleVersion(models.Model):
    rule = models.ForeignKey(CBRule, on_delete=models.CASCADE, related_name="versions")
    snapshot = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
