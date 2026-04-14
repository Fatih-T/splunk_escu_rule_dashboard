import csv
from django.http import HttpResponse
def export_rules_csv(queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="escu_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['rule_id', 'name', 'status'])
    for rule in queryset: writer.writerow([rule.rule_id, rule.name, rule.status])
    return response
