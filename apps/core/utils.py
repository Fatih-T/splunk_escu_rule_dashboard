from .models import AuditLog
def audit_log(action, entity_type, entity_id, entity_label, detail="", actor="system"):
    AuditLog.objects.create(action=action, entity_type=entity_type, entity_id=entity_id, entity_label=entity_label, actor_name=actor, detail=detail)
