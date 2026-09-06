from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Officer
from app.schemas import OfficerCreate, Token
from app.security.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register_officer(payload: OfficerCreate, db: Session = Depends(get_db)):
    existing = db.query(Officer).filter(Officer.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    officer = Officer(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(officer)
    db.commit()
    return {"message": "Officer registered", "username": officer.username, "role": officer.role}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    officer = db.query(Officer).filter(Officer.username == form_data.username).first()
    if not officer or not verify_password(form_data.password, officer.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": officer.username, "role": officer.role})
    return {"access_token": token, "token_type": "bearer"}