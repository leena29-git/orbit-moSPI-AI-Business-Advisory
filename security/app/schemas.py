from pydantic import BaseModel

class OfficerCreate(BaseModel):
    username: str
    password: str
    role: str = "viewer"

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileCreate(BaseModel):
    profile_id: str
    district_id: str
    block_id: str
    business_type: str
    capital_available: str
    expenses: str
    trade_skill: str
    language_dialect: str

class DPRStatusUpdate(BaseModel):
    status: str   # approved / rejected