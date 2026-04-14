from django.db import models

class RuleConversion(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("in_review", "In Review"), ("approved", "Approved"), ("rejected", "Rejected")]
    escu_rule = models.ForeignKey("escu.ESCURule", on_delete=models.CASCADE, related_name="conversions")
    cb_rule = models.ForeignKey("carbonblack.CBRule", on_delete=models.SET_NULL, null=True, blank=True, related_name="conversion_record")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    adaptation_notes = models.TextField(blank=True)
    cb_query_draft = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    created_by = models.CharField(max_length=150, default="system")
    reviewed_by = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"Conversion: {self.escu_rule.name} -> CB"

class SimilarityRecord(models.Model):
    COMPARE_TYPE = [("escu_escu", "ESCU <-> ESCU"), ("escu_cb", "ESCU <-> CB"), ("cb_cb", "CB <-> CB")]
    compare_type = models.CharField(max_length=10, choices=COMPARE_TYPE)
    rule_a_type = models.CharField(max_length=10)
    rule_a_id = models.IntegerField()
    rule_a_label = models.CharField(max_length=500)
    rule_b_type = models.CharField(max_length=10)
    rule_b_id = models.IntegerField()
    rule_b_label = models.CharField(max_length=500)
    score = models.FloatField()
    match_fields = models.JSONField(default=list)
    computed_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-score"]
        indexes = [models.Index(fields=["rule_a_type", "rule_a_id"]), models.Index(fields=["score"])]
    def __str__(self): return f"{self.rule_a_label} <-> {self.rule_b_label} ({self.score})"
