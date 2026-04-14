import csv
from django.http import HttpResponse
from apps.core.models import SystemConfig

DEFAULT_COLUMNS = [
    "rule_id", "name", "status", "severity",
    "mitre_tactic", "mitre_technique", "mitre_technique_id",
    "data_source", "assigned_analyst", "created_at",
]

def export_rules_csv(queryset, columns=None):
    if columns is None:
        config_cols = SystemConfig.get("export_columns_escu", "")
        columns = [c.strip() for c in config_cols.split(",") if c.strip()] or DEFAULT_COLUMNS

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="escu_rules_export.csv"'
    response.write("\ufeff")  # BOM for Turkish Excel compatibility

    writer = csv.DictWriter(response, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for rule in queryset:
        row = {col: getattr(rule, col, "") for col in columns}
        if "created_at" in row and rule.created_at:
            row["created_at"] = rule.created_at.strftime("%Y-%m-%d")
        writer.writerow(row)

    return response
