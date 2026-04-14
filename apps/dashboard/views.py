from django.shortcuts import render
from apps.escu.models import ESCURule
from apps.carbonblack.models import CBRule
def dashboard(request):
    return render(request, "dashboard/index.html", {"escu_active_count": ESCURule.objects.filter(status="active").count(), "cb_active_count": CBRule.objects.filter(status="active").count()})
