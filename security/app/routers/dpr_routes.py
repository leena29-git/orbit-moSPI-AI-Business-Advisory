from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EntrepreneurProfile, DPRRecord
from app.schemas import ProfileCreate, DPRStatusUpdate
from app.security.auth import get_current_officer, require_role
from app.security.encryption import encrypt_field, decrypt_field
from app.security.audit import log_action
from datetime import datetime

router = APIRouter(prefix="/dpr", tags=["dpr"])

@router.post("/profile")
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db),
                    officer=Depends(require_role("admin"))):
    profile = EntrepreneurProfile(
        profile_id=payload.profile_id,
        district_id=payload.district_id,
        block_id=payload.block_id,
        business_type=payload.business_type,
        capital_available_enc=encrypt_field(payload.capital_available),
        expenses_enc=encrypt_field(payload.expenses),
        trade_skill=payload.trade_skill,
        language_dialect=payload.language_dialect,
    )
    db.add(profile)
    db.commit()
    log_action(db, officer.username, officer.role, "CREATE_PROFILE", payload.profile_id)
    return {"message": "Profile created (sensitive fields encrypted)"}

@router.get("/profile/{profile_id}")
def get_profile(profile_id: str, db: Session = Depends(get_db),
                 officer=Depends(get_current_officer)):
    profile = db.query(EntrepreneurProfile).filter_by(profile_id=profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Not found")
    log_action(db, officer.username, officer.role, "VIEW_PROFILE", profile_id)
    return {
        "profile_id": profile.profile_id,
        "district_id": profile.district_id,
        "business_type": profile.business_type,
        "capital_available": decrypt_field(profile.capital_available_enc),
        "expenses": decrypt_field(profile.expenses_enc),
    }

@router.put("/{dpr_id}/status")
def update_dpr_status(dpr_id: str, payload: DPRStatusUpdate, db: Session = Depends(get_db),
                       officer=Depends(require_role("approver", "admin"))):
    dpr = db.query(DPRRecord).filter_by(dpr_id=dpr_id).first()
    if not dpr:
        raise HTTPException(status_code=404, detail="DPR not found")
    dpr.status = payload.status
    dpr.reviewed_by = officer.username
    dpr.reviewed_at = datetime.utcnow()
    db.commit()
    log_action(db, officer.username, officer.role, f"DPR_{payload.status.upper()}", dpr_id)
    return {"message": f"DPR {dpr_id} marked {payload.status}"}