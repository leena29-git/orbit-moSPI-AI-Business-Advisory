from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Officer(Base):
    __tablename__ = "officers"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="viewer")   # viewer / approver / admin

class EntrepreneurProfile(Base):
    __tablename__ = "profiles"
    profile_id = Column(String, primary_key=True, index=True)
    district_id = Column(String)
    block_id = Column(String)
    business_type = Column(String)
    capital_available_enc = Column(String)     # encrypted
    expenses_enc = Column(String)               # encrypted
    trade_skill = Column(String)
    language_dialect = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DPRRecord(Base):
    __tablename__ = "dpr_records"
    dpr_id = Column(String, primary_key=True, index=True)
    profile_id = Column(String, ForeignKey("profiles.profile_id"))
    matched_scheme = Column(String)
    status = Column(String, default="draft")   # draft/pending_review/approved/rejected
    reviewed_by = Column(String, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(String)
    actor_role = Column(String)
    action = Column(String)
    target_record_id = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())