from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from apps.escu.models import ESCURule, PIPELINE_STAGES
from apps.carbonblack.models import CBRule
from apps.core.models import AuditLog, SystemConfig
from apps.pipeline.models import SimilarityRecord
from apps.analysis.models import ANALYST_CHOICES

def dashboard(request):
    sla = int(SystemConfig.get("review_sla_days", "14"))
    now = timezone.now()
    context = {
        "escu_active_count": ESCURule.objects.filter(status="active").count(),
        "cb_active_count": CBRule.objects.filter(status="active").count(),
        "this_month_count": ESCURule.objects.filter(created_at__month=now.month, created_at__year=now.year).count(),
        "unassigned_count": ESCURule.objects.filter(assigned_analyst="").count(),
        "pipeline_summary": [{"stage": s[1], "count": ESCURule.objects.filter(status=s[0]).count()} for s in PIPELINE_STAGES],
        "analyst_load": [{"name": a[1], "escu_count": ESCURule.objects.filter(assigned_analyst=a[0]).count(), "cb_count": CBRule.objects.filter(assigned_analyst=a[0]).count()} for a in ANALYST_CHOICES],
        "sla_overdue_count": ESCURule.objects.filter(status="under_review", updated_at__lt=now - timedelta(days=sla)).count(),
        "high_similarity": SimilarityRecord.objects.filter(score__gte=0.70).order_by("-score")[:10],
        "recent_logs": AuditLog.objects.all()[:5],
    }
    return render(request, "dashboard/index.html", context)
