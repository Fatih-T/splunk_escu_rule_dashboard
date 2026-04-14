import csv
from .models import ESCURule, ESCURuleVersion, ESCUImportBatch
from apps.core.utils import audit_log
from apps.core.models import SystemConfig
def process_escu_import(batch_id, column_mapping):
    batch = ESCUImportBatch.objects.get(pk=batch_id)
    actor = SystemConfig.get("default_analyst", "system")
    try:
        with batch.file_path.open('r') as f:
            reader = csv.DictReader(f)
            seen_ids = []
            for row in reader:
                rule_data = {f: row[c] for f, c in column_mapping.items() if c and c in row}
                rid = rule_data.get('rule_id')
                if not rid: continue
                seen_ids.append(rid)
                rule, created = ESCURule.objects.get_or_create(rule_id=rid, defaults={'name': rule_data.get('name', rid), 'raw_csv_row': row, 'first_seen_batch': batch, 'last_seen_batch': batch})
                if created: batch.rules_added += 1
                else:
                    ESCURuleVersion.objects.create(rule=rule, batch=batch, snapshot=rule.raw_csv_row, change_summary="Import update")
                    for k,v in rule_data.items(): setattr(rule, k, v)
                    rule.raw_csv_row = row; rule.last_seen_batch = batch; rule.save()
                    batch.rules_updated += 1
            deprecated = ESCURule.objects.exclude(rule_id__in=seen_ids).exclude(status="deprecated")
            batch.rules_deprecated = deprecated.count()
            deprecated.update(status="deprecated")
            batch.status = "processed"; batch.save()
            audit_log("import", "ESCUImportBatch", batch.pk, batch.filename, actor=actor)
    except Exception as e:
        batch.status = "failed"; batch.save()
        raise e
