from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CBRule
from .filters import CBRuleFilter
from .csv_exporter import export_cb_rules_csv
from apps.core.utils import audit_log

def rule_list(request):
    f = CBRuleFilter(request.GET, queryset=CBRule.objects.all())
    if request.method == "POST":
        action = request.POST.get("bulk_action")
        qs = CBRule.objects.filter(pk__in=request.POST.getlist("row_checkbox"))
        if action == "export_csv": return export_cb_rules_csv(qs)
        elif action == "change_status": qs.update(status=request.POST.get("new_status"))
        elif action == "assign": qs.update(assigned_analyst=request.POST.get("analyst"))
        return redirect("cb_list")
    return render(request, "carbonblack/list.html", {"filter": f})

def rule_detail(request, pk):
    r = get_object_or_404(CBRule, pk=pk)
    return render(request, "carbonblack/detail.html", {"rule": r, "versions": r.versions.all()[:10]})

def rule_create(request):
    if request.method == "POST":
        r = CBRule.objects.create(name=request.POST.get("name"), rule_id=request.POST.get("rule_id"), description=request.POST.get("description", ""), query=request.POST.get("query", ""), severity=request.POST.get("severity", ""), mitre_tactic=request.POST.get("mitre_tactic", ""), mitre_technique_id=request.POST.get("mitre_technique_id", ""), assigned_analyst=request.POST.get("assigned_analyst", ""))
        audit_log("create", "CBRule", r.pk, r.name); return redirect("cb_detail", pk=r.pk)
    return render(request, "carbonblack/create.html")

def rule_edit(request, pk):
    r = get_object_or_404(CBRule, pk=pk)
    if request.method == "POST":
        r.name = request.POST.get("name", r.name); r.description = request.POST.get("description", r.description); r.query = request.POST.get("query", r.query); r.severity = request.POST.get("severity", r.severity); r.assigned_analyst = request.POST.get("assigned_analyst", r.assigned_analyst)
        r.save(); audit_log("update", "CBRule", r.pk, r.name); return redirect("cb_detail", pk=r.pk)
    return render(request, "carbonblack/edit.html", {"rule": r})

def rule_delete(request, pk):
    r = get_object_or_404(CBRule, pk=pk)
    if request.method == "POST": audit_log("delete", "CBRule", r.pk, r.name); r.delete(); return redirect("cb_list")
    return render(request, "carbonblack/confirm_delete.html", {"rule": r})
