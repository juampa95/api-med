from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routers import router_medicine
from api.routers import router_patient
from api.routers import router_doctor
from api.routers import router_prescription
from api.routers import router_prescriptionDetails
from api.routers import router_unidosis
from api.routers import router_users
from api.routers import router_dispensePrescription
from api.db import get_session
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from sqlalchemy.sql import text

app = FastAPI()
origin = ['*']

app.add_middleware(CORSMiddleware,
                   allow_origins=origin,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*']
                   )

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


app.include_router(router_medicine.router, tags=["Medicine"])
app.include_router(router_patient.router, tags=["Patient"])
app.include_router(router_doctor.router, tags=["Doctor"])
app.include_router(router_prescription.router, tags=["Prescription"])
app.include_router(router_prescriptionDetails.router, tags=["Prescription"])
app.include_router(router_unidosis.router, tags=["Unidosis"])
app.include_router(router_dispensePrescription.router, tags=["Dispense"])
app.include_router(router_users.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

