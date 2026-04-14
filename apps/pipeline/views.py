from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from apps.escu.models import ESCURule
from apps.carbonblack.models import CBRule
from .models import RuleConversion
from apps.core.utils import audit_log

ORDERED_STAGES = ["new", "under_review", "not_applicable", "applicable", "in_progress", "ready_for_cb", "converted", "active", "tuning", "deprecated"]
ALLOWED_TRANSITIONS = {
    "new": ["under_review"],
    "under_review": ["not_applicable", "applicable"],
    "applicable": ["in_progress"],
    "in_progress": ["ready_for_cb", "under_review"],
    "ready_for_cb": ["converted"],
    "converted": ["active"],
    "active": ["tuning", "deprecated"],
    "tuning": ["active", "deprecated"],
    "not_applicable": ["under_review"],
}

def pipeline_board(request):
    rt = request.GET.get("type", "escu")
    board = {s: {"escu": ESCURule.objects.filter(status=s) if rt in ("escu", "all") else [], "cb": CBRule.objects.filter(status=s) if rt in ("cb", "all") else []} for s in ORDERED_STAGES}
    return render(request, "pipeline/board.html", {"board": board, "stages": ORDERED_STAGES, "rule_type": rt})

def stage_transition(request, type, pk):
    if request.method != "POST": return HttpResponseBadRequest("Only POST")
    ns = request.POST.get("new_stage")
    model = ESCURule if type == "escu" else CBRule
    obj = get_object_or_404(model, pk=pk)
    if ns not in ALLOWED_TRANSITIONS.get(obj.status, []):
        audit_log("stage_change", type, obj.pk, str(obj), detail=f"Invalid transition attempt: {obj.status} -> {ns}")
        return HttpResponseBadRequest(f"Invalid transition: {obj.status} -> {ns}")
    old = obj.status; obj.status = ns; obj.save()
    audit_log("stage_change", type, obj.pk, str(obj), detail=f"{old} -> {ns}")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def convert_wizard(request, escu_pk):
    escu = get_object_or_404(ESCURule, pk=escu_pk)
    if request.method == "POST":
        step = int(request.POST.get("step", 1))
        if step == 1:
            if request.POST.get("applicable") == "no":
                escu.not_applicable_reason = request.POST.get("not_applicable_reason", "")
                escu.status = "not_applicable"; escu.save()
                audit_log("stage_change", "escu", escu.pk, escu.name, detail="Marked as not_applicable")
                return redirect("escu_list")
            return render(request, "pipeline/convert_wizard.html", {"escu_rule": escu, "step": 2})
        elif step == 2:
            conv, _ = RuleConversion.objects.get_or_create(escu_rule=escu)
            conv.cb_query_draft = request.POST.get("cb_query_draft", "")
            conv.adaptation_notes = request.POST.get("adaptation_notes", "")
            conv.save()
            return render(request, "pipeline/convert_wizard.html", {"escu_rule": escu, "step": 3, "conversion": conv})
        elif step == 3:
            conv = get_object_or_404(RuleConversion, escu_rule=escu)
            import uuid
            cb = CBRule.objects.create(name=f"CB: {escu.name}", rule_id=f"CB-{escu.rule_id[:50]}-{str(uuid.uuid4())[:8]}", description=escu.description, query=conv.cb_query_draft, severity=escu.severity, mitre_tactic=escu.mitre_tactic, mitre_technique=escu.mitre_technique, mitre_technique_id=escu.mitre_technique_id, source_escu_rule=escu, status="new")
            conv.cb_rule = cb; conv.status = "approved"; conv.save()
            escu.status = "converted"; escu.save()
            audit_log("convert", "escu", escu.pk, escu.name, detail=f"Converted to CB #{cb.pk}")
            return redirect("cb_detail", pk=cb.pk)
    return render(request, "pipeline/convert_wizard.html", {"escu_rule": escu, "step": 1})

def conversion_detail(request, pk):
    return render(request, "pipeline/conversion_detail.html", {"conversion": get_object_or_404(RuleConversion, pk=pk)})
