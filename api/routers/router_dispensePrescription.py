from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from api.models.prescription_details_model import PrescriptionDetails
from api.models.perscription_model import Prescription
from api.models.medicine_model import Medicine, DispenseMedicine, StockMedicine, Status, MovementType, StockMovements
from api.db import get_session
from typing import List, Optional


router = APIRouter(prefix="/dispensePrescription")

@router.post("/dispense")
async def create_dispense(prescription_id: int,
                          data: List[DispenseMedicine],
                          session: Session = Depends(get_session)):
    try:
        prescription_details = session.query(PrescriptionDetails).filter_by(prescription_id=prescription_id).all()

        for details in prescription_details:
            medicine_id = details.medicine_id
            qty = details.qty

            medicine = session.query(Medicine).filter_by(id=medicine_id).first()
            med_stock = medicine.stock

            if med_stock < qty:
                raise HTTPException(
                    status_code=404,
                    detail=f"La cantidad de {medicine.name} en stock no es suficiente")

        if not data:
            # FALTA ver como le asigno seriales si no se le pasa ninguno como entrada.
            # La idea era asignarle el primero que entro, entonces daria de baja el mas viejo.
            # Igualmente, esto no funcionaria asi, ya que obligadamente tendria que pasar un serial.
            pass
        else:
            for details in prescription_details:
                for item in data:
                    if (
                            item.medicine_id == details.medicine_id
                            and details.qty == len(item.serials)
                    ):
                        for serial in item.serials:
                            medicine_dispensed = session.query(StockMedicine).filter_by(medicine_id=item.medicine_id,
                                                                                    serial=serial,
                                                                                    status=Status.AVAILABLE).first()
                            medicine_dispensed.status = Status.DISPENSED

                            stock_movement = StockMovements(
                                stock_medicine_id=medicine_dispensed.id,  # Asegúrate de tener el stock_medicine.id correcto
                                movement_type=MovementType.DISPENSE  # Otra variable que defina el tipo de movimiento
                            )
                            session.add(stock_movement)
                            session.commit()
                    else:
                        raise  HTTPException(
                    status_code=404,
                    detail=f"No se proporcionaron seriales para el medicamento con el ID:{item.medicine_id}"
                           f"o la cantidad proporcionada no es suficiente, necesita {details.qty} y se "
                           f"proporcionaron {len(item.serials)}")

    except HTTPException as e:
        raise e