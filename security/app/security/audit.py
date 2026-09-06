from sqlalchemy.orm import Session
from app.models import AuditLog

def log_action(db: Session, actor_id: str, actor_role: str, action: str, target_record_id: str):
    entry = AuditLog(
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        target_record_id=target_record_id,
    )
    db.add(entry)
    db.commit()