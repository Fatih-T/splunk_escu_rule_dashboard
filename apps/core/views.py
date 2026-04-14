from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import SystemConfig, AuditLog
from .utils import audit_log
def config_list(request):
    return render(request, "core/config_list.html", {"configs": SystemConfig.objects.all()})
def config_edit(request, pk):
    config = get_object_or_404(SystemConfig, pk=pk)
    if request.method == "POST":
        config.value = request.POST.get("value")
        config.save()
        audit_log("update", "SystemConfig", config.pk, config.get_key_display(), actor=SystemConfig.get("default_analyst", "system"))
        messages.success(request, f"{config.get_key_display()} güncellendi.")
        return redirect("config_list")
    return render(request, "core/config_edit.html", {"config": config})
def audit_log_list(request):
    return render(request, "core/audit_log_list.html", {"logs": AuditLog.objects.all()})
