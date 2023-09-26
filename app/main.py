from fastapi import FastAPI
import uvicorn
from app.routers import router_medicine
from app.routers import router_patient
from app.routers import router_doctor
from app.routers import router_prescription
from app.routers import router_prescriptionDetails
from app.routers import router_unidosis
from app.routers import router_users
from app.db import get_session
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from sqlalchemy.sql import text

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "!Server up! REST API for medical prescription. Check documentations in: ../docs"}


@app.get("/db_version")
async def get_db_version(session: Session = Depends(get_session)):
    sql = text("SELECT version_num FROM alembic_version")
    result = session.execute(sql)
    versions = [row[0] for row in result.fetchall()]
    session.close()

    return {"last version": versions}


app.include_router(router_medicine.router)
app.include_router(router_patient.router)
app.include_router(router_doctor.router)
app.include_router(router_prescription.router)
app.include_router(router_prescriptionDetails.router)
app.include_router(router_unidosis.router)
app.include_router(router_users.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

