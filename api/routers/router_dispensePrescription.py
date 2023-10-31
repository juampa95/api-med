from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, asc
from api.models.prescription_details_model import PrescriptionDetails
from api.models.perscription_model import Prescription, PrescriptionStatus
from api.models.medicine_model import Medicine, DispenseMedicine, StockMedicine, Status, MoveType, StockMovements
from api.db import get_session
from typing import List, Optional

router = APIRouter(prefix="/dispensePrescription")


@router.post("/dispense",
             summary="Dispensar medicamentos según receta",
             description="Ofrece dos modos de funcionamiento, pero siempre se debe proporcionar el id de la receta.  "
                         "Consultar el Schema DispenseMedicine para mas información")
async def create_dispense(prescription_id: int,
                          data: Optional[List[DispenseMedicine]],
                          session: Session = Depends(get_session)):
    try:
        prescription = session.query(Prescription).filter_by(id=prescription_id).first()
        if prescription.status != PrescriptionStatus.CREATED:
            raise HTTPException(status_code=400, detail="La receta no se puede dispensar en su estado actual.")

        prescription_details = session.query(PrescriptionDetails).filter_by(prescription_id=prescription_id).all()
        if not prescription_details:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron detalles de receta para la receta con ID: {prescription_id}"
            )

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
            # En caso de que no se pase informacion de los seriales de los medicamentos que van en la
            # receta, se asignara automaticamente el primero que se ingreso al stock que este disponible.
            # Esto se puede modificar para que se seleccione un medicamento proximo a vencerse.
            for details in prescription_details:
                for _ in range(details.qty):
                    oldest_med = (session.query(StockMedicine)
                                  .filter_by(medicine_id=details.medicine_id,
                                             status=Status.AVAILABLE
                                             )
                                  .order_by(asc(StockMedicine.created_at)).limit(details.qty).first()
                                  )
                    oldest_med.status = Status.DISPENSED
                    oldest_med.prescription_id = prescription_id

                    # Después de cambiar el status en el stock, vamos a completar el registro de movimientos.
                    stock_movement = StockMovements(
                        stock_medicine_id=oldest_med.id,
                    )
                    session.add(stock_movement)

                    # Cambiar el valor de movement_type aquí
                    stock_movement.movement_type = MoveType.DISPENSE
                    session.commit()

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
                            medicine_dispensed.prescription_id = prescription_id

                            stock_movement = StockMovements(
                                stock_medicine_id=medicine_dispensed.id,  # Asegúrate de tener el stock_medicine.id correcto
                                movement_type=MoveType.DISPENSE  # Otra variable que defina el tipo de movimiento
                            )
                            session.add(stock_movement)
                            session.commit()
                    else:
                        raise  HTTPException(
                    status_code=404,
                    detail=f"No se proporcionaron seriales para el medicamento con el ID:{item.medicine_id}"
                           f"o la cantidad proporcionada no es suficiente, necesita {details.qty} y se "
                           f"proporcionaron {len(item.serials)}")

        prescription.status = PrescriptionStatus.DISPENSED
        session.commit()

        return {"message": "Receta dispensada correctamente, "
                           "Medicamentos asignados exitosamente"}

    except HTTPException as e:
        raise e

