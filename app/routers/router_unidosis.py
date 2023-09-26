from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from app import models_unidosis
from app.models_unidosis import UnidosisMedicine as model
from app.db import get_session
from app.models import Medicine

router = APIRouter(prefix="/unidosis")

@router.get("/list")
async def get_unidosis_list(session: Session = Depends(get_session)):
    try:
        statement = select(model)
        objet = session.exec(statement).all()
        return objet
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e  # Esto volverá a lanzar la excepción para obtener más información detallada en la respuesta



@router.get("/{object_id}")
async def get_unidosis_details(object_id: int, session: Session = Depends(get_session)):
    try:
        unidosis = session.query(model).filter_by(id=object_id).first()
        if not unidosis:
            raise HTTPException(status_code=404, detail="Unidosis not found")

        medicine = session.query(Medicine).filter_by(id=unidosis.medicine_id).first()

        medicine_info = {
            "code": medicine.code,
            "name": medicine.name,
            "drug": medicine.drug,
            "concentration": medicine.concentration
        }

        response = {
            "unidosis" : unidosis,
            "medicine": medicine_info
        }
    except:
        raise HTTPException(status_code=404, detail="unidosis details not found")
    # statement = select(model).where(model.id == object_id)
    # object = session.exec(statement).first()
    # if object is None:
    #     raise HTTPException(status_code=404, detail="unidosis details not found")
    # return object
    return response

@router.post("/create")
async def create_unidosis_model(object: model, session: Session = Depends(get_session)):
    session.add(object)
    session.commit()
    session.refresh(object)
    return object