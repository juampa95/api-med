from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlmodel import Session, select
from app import models
from app.models import Prescription as model
from app.models import PrescriptionDetails as prescriptionDetailsModel
from app.models import PrescriptionDetailsResponse
from app.db import get_session
from datetime import datetime

router = APIRouter(prefix="/prescription")


@router.get("/list", response_model=List[model])
async def get_prescriptions(session: Session = Depends(get_session)):
    try:
        statement = select(model)
        objet = session.exec(statement).all()
        return objet
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e  # Esto volverá a lanzar la excepción para obtener más información detallada en la respuesta


@router.get("/{prescription_id}", response_model=model)
async def get_prescription(object_id: int, session: Session = Depends(get_session)):
    statement = select(model).where(model.id == object_id)
    object = session.exec(statement).first()
    if object is None:
        raise HTTPException(status_code=404, detail="prescription not found")
    return object


@router.post("/create", response_model=model)
async def create_prescription(object: model, session: Session = Depends(get_session)):
    session.add(object)
    session.commit()
    session.refresh(object)
    return object


@router.get("/prescription_details/{prescription_id}", response_model=PrescriptionDetailsResponse)
async def get_prescription_details(prescription_id: int, session: Session = Depends(get_session)):
    try:
        # Consulta a tabla de prescripciones
        prescription = session.query(model).filter_by(id=prescription_id).first()
        # Consulta a tabla de detalle de prescripciones
        prescription_details = session.query(prescriptionDetailsModel).filter_by(prescription_id=prescription_id).all()

        if not prescription:
            raise HTTPException(status_code=404, detail="Prescription not found")

        patient_info = {
            "name": prescription.patient.name,
            "lastname": prescription.patient.lastname,
            "personal_id": prescription.patient.personal_id
        }

        doctor_info = {
            "name": prescription.doctor.name,
            "lastname": prescription.doctor.lastname,
            "personal_id": prescription.doctor.personal_id
        }

        recipe = [{
            "medicine": pd.medicine.name,
            "concentration": pd.medicine.concentration,
            "qty": pd.qty
        }
            for pd in prescription_details
        ]

        response = PrescriptionDetailsResponse(
            id=prescription.id,
            code=prescription.code,
            recipe_created_at=prescription.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            patient=patient_info,
            doctor=doctor_info,
            recipe=recipe
        )

        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")