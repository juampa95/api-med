from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
# from api.models import models
from api.models.medicine_model import Medicine as model
from api.db import get_session  # Importa la función get_session desde db.py

router = APIRouter(prefix="/medicine")

@router.get("/list", response_model=List[model],
            summary="Obtener una lista de medicamentos",
            description="Esta ruta devuelve una lista de los medicamentos disponibles.")
async def get_medicines(session: Session = Depends(get_session)):
    try:
        statement = select(model)
        medicines = session.exec(statement).all()
        return medicines
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e  # Esto volverá a lanzar la excepción para obtener más información detallada en la respuesta


@router.get("/{medicine_id}", response_model=model)
async def get_medicine(medicine_id: int, session: Session = Depends(get_session)):
    statement = select(model).where(model.id == medicine_id)
    medicine = session.exec(statement).first()
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.post("/create", response_model=model)
async def create_medicine(medicine: model, session: Session = Depends(get_session)):
    session.add(medicine)
    session.commit()
    session.refresh(medicine)
    return medicine
