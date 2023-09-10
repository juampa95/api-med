from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from app import models
from app.models import PrescriptionDetails as model
from app.db import get_session  # Importa la función get_session desde db.py

router = APIRouter(prefix="/prescriptionDetails")


@router.get("/list", response_model=List[model])
async def get_prescriptionsDetails(session: Session = Depends(get_session)):
    try:
        statement = select(model)
        objet = session.exec(statement).all()
        return objet
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e  # Esto volverá a lanzar la excepción para obtener más información detallada en la respuesta


@router.get("/{prescriptionDetail_id}", response_model=model)
async def get_prescriptionDetail(object_id: int, session: Session = Depends(get_session)):
    statement = select(model).where(model.id == object_id)
    object = session.exec(statement).first()
    if object is None:
        raise HTTPException(status_code=404, detail="prescription details not found")
    return object

@router.post("/create", response_model=model)
async def create_prescriptionDetail(object: model, session: Session = Depends(get_session)):
    session.add(object)
    session.commit()
    session.refresh(object)
    return object
