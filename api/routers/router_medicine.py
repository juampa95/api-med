from fastapi import APIRouter, HTTPException, Depends, UploadFile
from typing import List

from sqlmodel import Session, select, func, and_
# from api.models import models
from api.models.medicine_model import Medicine as model
from api.models.medicine_model import StockMedicine, LoadStockMedicine, Status
from api.db import get_session  # Importa la función get_session desde db.py
from api.repos.medicine_load import validate_medicine, check_duplicate_medicine, get_stock

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


# CARGA DE MEDICAMENTOS A PARTIR DE EXCEL.
@router.post("/upload_excel")
async def upload_file(file: UploadFile, session: Session = Depends(get_session)):
    medicine_dict = validate_medicine(file)
    medicine_list = []

    for item in medicine_dict:
        medicine = model(**item)
        session.add(medicine)
        session.commit()
        session.refresh(medicine)
        medicine_list.append(medicine)

    return {"message": "Archivo cargado exitosamente",
            "data": medicine_dict}


@router.post("/load")
async def load_medicine(load_medicine: LoadStockMedicine, session: Session = Depends(get_session)):
    medicine = session.get(model, load_medicine.medicine_id)  # Buscamos que exista ese medicine_id
    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="El medicamento no existe")

    try:
        # with session.begin():
            for serial in load_medicine.serial:
                existing_medicine = check_duplicate_medicine(session, load_medicine.medicine_id, serial)

                if existing_medicine:
                    raise HTTPException(
                        status_code=400,
                        detail="Ya existe un medicamento con el mismo medicine_id y serial.",
                    )

                stock_medicine = StockMedicine(
                    medicine_id=load_medicine.medicine_id,
                    status=load_medicine.status,
                    movement_type=load_medicine.movement_type,
                    serial=serial,
                )

                session.add(stock_medicine)
                session.commit()

            in_stock = get_stock(session, load_medicine.medicine_id, Status.AVAILABLE)

            if in_stock is None:
                in_stock = 0

            if in_stock < 0:
                raise HTTPException(status_code=404, detail="Error en control de stock")

            # Actualizamos el stock
            medicine.stock = in_stock
            session.add(medicine)
            session.commit()

            return {"message": "Medicamento cargado exitosamente al stock"}
    except Exception as e:
        # session.rollback()
        raise e
