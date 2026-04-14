import csv, io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ESCURule, ESCUImportBatch, ESCURuleVersion
from .filters import ESCURuleFilter
from .csv_parser import process_escu_import
from .csv_exporter import export_rules_csv
from .similarity import rule_similarity
from apps.pipeline.models import SimilarityRecord
from apps.core.models import SystemConfig, AuditLog
from apps.analysis.models import Note

def rule_list(request):
    f = ESCURuleFilter(request.GET, queryset=ESCURule.objects.all())
    if request.method == "POST":
        action = request.POST.get("bulk_action")
        qs = ESCURule.objects.filter(pk__in=request.POST.getlist("row_checkbox"))
        if action == "export_csv": return export_rules_csv(qs)
        elif action == "change_status": qs.update(status=request.POST.get("new_status"))
        elif action == "assign": qs.update(assigned_analyst=request.POST.get("analyst"))
        return redirect("escu_list")
    return render(request, "escu/list.html", {"filter": f})

def rule_detail(request, pk):
    rule = get_object_or_404(ESCURule, pk=pk)
    context = {"rule": rule, "notes": Note.objects.filter(rule_type="escu", rule_id=pk), "audit_logs": AuditLog.objects.filter(entity_type="escu", entity_id=pk), "versions": rule.versions.all(), "conversions": rule.cb_conversions.all()}
    return render(request, "escu/detail.html", context)

def import_csv(request):
    if request.method == "POST":
        if 'csv_file' in request.FILES:
            f = request.FILES['csv_file']
            b = ESCUImportBatch.objects.create(filename=f.name, file_path=f)
            h = next(csv.reader(io.StringIO(f.read().decode('utf-8'))))
            return render(request, "escu/import_mapping.html", {"batch": b, "headers": h, "model_fields": ['rule_id', 'name', 'description', 'mitre_tactic', 'mitre_technique', 'mitre_technique_id', 'severity', 'search', 'data_source']})
        elif 'batch_id' in request.POST:
            m = {k.replace('map_', ''): v for k, v in request.POST.items() if k.startswith('map_')}
            process_escu_import(request.POST.get('batch_id'), m)
            return redirect("escu_batches")
    return render(request, "escu/import.html")

def batch_list(request):
    return render(request, "escu/batch_list.html", {"batches": ESCUImportBatch.objects.all().order_by('-imported_at')})

def batch_diff(request, pk):
    b = get_object_or_404(ESCUImportBatch, pk=pk)
    return render(request, "escu/diff.html", {"batch": b, "new_rules": b.new_rules.all()})

def similarity_list(request):
    return render(request, "escu/similarity.html", {"records": SimilarityRecord.objects.filter(compare_type="escu_cb")})

def compute_similarity_view(request):
    if request.method != "POST":
        return redirect("escu_similarity")

    from apps.carbonblack.models import CBRule
    from apps.pipeline.models import SimilarityRecord
    from .similarity import rule_similarity
    from apps.core.models import SystemConfig

    threshold = float(SystemConfig.get("similarity_threshold", "70")) / 100.0
    SimilarityRecord.objects.filter(compare_type="escu_cb").delete()

    escu_rules = list(ESCURule.objects.exclude(status="deprecated"))
    cb_rules = list(CBRule.objects.exclude(status="deprecated"))
    created = 0

    for er in escu_rules:
        for cr in cb_rules:
            score, matched = rule_similarity(
                {
                    "name": er.name,
                    "mitre_technique_id": er.mitre_technique_id,
                    "mitre_tactic": er.mitre_tactic,
                    "data_source": er.data_source,
                    "description": er.description,
                },
                {
                    "name": cr.name,
                    "mitre_technique_id": cr.mitre_technique_id,
                    "mitre_tactic": cr.mitre_tactic,
                    "data_source": "",
                    "description": cr.description,
                }
            )
            if score >= threshold:
                SimilarityRecord.objects.create(
                    compare_type="escu_cb",
                    rule_a_type="escu", rule_a_id=er.pk, rule_a_label=er.name,
                    rule_b_type="cb",   rule_b_id=cr.pk, rule_b_label=cr.name,
                    score=score, match_fields=matched,
                )
                created += 1

    messages.success(request, f"{created} similarity records created.")
    return redirect("escu_similarity")
