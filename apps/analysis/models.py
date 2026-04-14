from django.db import models
ANALYST_CHOICES = [("analyst_1", "Analyst 1"), ("analyst_2", "Analyst 2"), ("analyst_3", "Analyst 3"), ("analyst_4", "Analyst 4"), ("analyst_5", "Analyst 5")]
class RuleAssignment(models.Model):
    RULE_TYPE_CHOICES = [("escu", "ESCU"), ("cb", "Carbon Black")]
    rule_type = models.CharField(max_length=10, choices=RULE_TYPE_CHOICES)
    rule_id = models.IntegerField()
    rule_label = models.CharField(max_length=500)
    analyst = models.CharField(max_length=150, choices=ANALYST_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f"{self.rule_label} -> {self.analyst}"

class Note(models.Model):
    RULE_TYPE_CHOICES = [("escu", "ESCU"), ("cb", "Carbon Black")]
    rule_type = models.CharField(max_length=10, choices=RULE_TYPE_CHOICES)
    rule_id = models.IntegerField()
    rule_label = models.CharField(max_length=500)
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.CharField(max_length=150, choices=ANALYST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = Note.objects.get(pk=self.pk)
                if old.content != self.content:
                    NoteVersion.objects.create(note=self, content_snapshot=old.content, edited_by="system")
            except Note.DoesNotExist: pass
        super().save(*args, **kwargs)
    def __str__(self): return f"Note: {self.title} by {self.author}"

class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="versions")
    content_snapshot = models.TextField()
    edited_by = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]

class Comment(models.Model):
    RULE_TYPE_CHOICES = [("escu", "ESCU"), ("cb", "Carbon Black")]
    rule_type = models.CharField(max_length=10, choices=RULE_TYPE_CHOICES)
    rule_id = models.IntegerField()
    author = models.CharField(max_length=150, choices=ANALYST_CHOICES)
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["created_at"]
