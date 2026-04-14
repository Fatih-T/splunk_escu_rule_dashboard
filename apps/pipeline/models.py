from django.db import models
class RuleConversion(models.Model):
    escu_rule = models.ForeignKey("escu.ESCURule", on_delete=models.CASCADE, related_name="conversions")
    cb_rule = models.ForeignKey("carbonblack.CBRule", on_delete=models.SET_NULL, null=True, blank=True, related_name="conversion_record")
    adaptation_notes = models.TextField(blank=True)
    cb_query_draft = models.TextField(blank=True)
    status = models.CharField(max_length=20, default="draft")
class SimilarityRecord(models.Model):
    compare_type = models.CharField(max_length=10)
    rule_a_id = models.IntegerField()
    rule_a_label = models.CharField(max_length=500)
    rule_b_id = models.IntegerField()
    rule_b_label = models.CharField(max_length=500)
    score = models.FloatField()
    match_fields = models.JSONField(default=list)
