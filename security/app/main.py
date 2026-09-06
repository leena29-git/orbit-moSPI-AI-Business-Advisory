from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth_routes, dpr_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orbit — Module 5: Security & Compliance")

app.include_router(auth_routes.router)
app.include_router(dpr_routes.router)

@app.get("/")
def root():
    return {"status": "Orbit security service running"}