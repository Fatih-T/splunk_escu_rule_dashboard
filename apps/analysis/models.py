from django.db import models
ANALYST_CHOICES = [("analyst_1", "Analyst 1"), ("analyst_2", "Analyst 2")]
class RuleAssignment(models.Model):
    rule_type = models.CharField(max_length=10)
    rule_id = models.IntegerField()
    rule_label = models.CharField(max_length=500)
    analyst = models.CharField(max_length=150, choices=ANALYST_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
class Note(models.Model):
    rule_type = models.CharField(max_length=10)
    rule_id = models.IntegerField()
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="versions")
    content_snapshot = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Comment(models.Model):
    rule_type = models.CharField(max_length=10)
    rule_id = models.IntegerField()
    author = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
