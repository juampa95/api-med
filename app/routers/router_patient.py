from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from app import models
from app.models import Patient as model
from app.db import get_session  # Importa la función get_session desde db.py

router = APIRouter(prefix="/patient")


@router.get("/list", response_model=List[model])
async def get_patients(session: Session = Depends(get_session)):
    try:
        statement = select(model)
        objet = session.exec(statement).all()
        return objet
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e  # Esto volverá a lanzar la excepción para obtener más información detallada en la respuesta


@router.get("/{patient_id}", response_model=model)
async def get_patient(object_id: int, session: Session = Depends(get_session)):
    statement = select(model).where(model.id == object_id)
    object = session.exec(statement).first()
    if object is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return object


@router.get("/dni/{patient_personal_id}",response_model=model)
async def query_patient_by_personal_id(patient_personal_id: int, session: Session = Depends(get_session)):
    statement = select(model).where(model.personal_id == patient_personal_id)
    object = session.exec(statement).first()
    if object is None:
        raise HTTPException(status_code=404, detail=f'Patient with personal ID {patient_personal_id} not found')
    return object


@router.post("/create", response_model=model)
async def create_patient(object: model, session: Session = Depends(get_session)):
    session.add(object)
    session.commit()
    session.refresh(object)
    return object
