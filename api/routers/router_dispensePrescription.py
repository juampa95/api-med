from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from api.models.prescription_details_model import PrescriptionDetails
from api.models.perscription_model import Prescription
from api.db import get_session

router = APIRouter(prefix="/dispensePrescription")

@router.post("/dispense")
async def create_dispense(prescription_id: int, session: Session = Depends(get_session)):
    try:
        prescription_details = session.query(PrescriptionDetails).filter_by(prescription_id=prescription_id).all()



    except HTTPException as e:
        raise e