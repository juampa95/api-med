import pandas as pd
import io
from api.models.medicine_model import StockMedicine, Status
from sqlmodel import select, func


def validate_medicine(file):
    """
    Esta funcion se usa para cargar archivos desde un excel que tiene que
    tener las columnas mencionadas mas abajo.
    :param file: archivo excel .xlsx
    :return: diccionario de medicnias segun la clase Medicine
    """
    file_content = io.BytesIO(file.file.read())
    df = pd.read_excel(file_content).head(150)

    # FORMATEO SEGUN EXCEL MODELO. VER COMO SE PUEDE CAMBIAR ESTO
    # Mi idea es que se pueda seleccionar las columnas del excel origen
    # y asignarles una columna destino de las que posee la tabla SQL.
    try:
        df = df.rename(columns={
            'TROQUEL': 'id',
            'MARCA': 'name',
            'MONODROGA': 'drug',
            'PRESENTACION': 'concentration',
            'CODIGO BARRAS': 'gtin',
            'HABILITADO (0)': 'hab'
        })
    except:
        return print('las columnas no existen o el nombre es incorrecto')


    df = df[
        df['gtin'].notnull() &
        (df['gtin'] != 0) &
        (df['hab'] == 0)
        ]

    df = df[['id', 'name', 'drug', 'concentration', 'gtin']]
    df['id'] = df['id'].astype(int)
    df['gtin'] = (df['gtin']
                  .astype(str)
                  .str.rstrip('.0'))

    medicine_dict = df.to_dict(orient="records")

    return medicine_dict


# print(validate_medicine('data/ALFABETA COMPLETO.xlsx'))


def check_duplicate_medicine(session, medicine_id, serial):
    """
    Esta funcion sirve para verificar que el medicamento que se va a ingresar
    al stock no se encuentra en el mismo, verificando el conjunto de
    medicine_id y serial.
    :param session:
    :param medicine_id:
    :param serial:
    :return:
    """
    return session.query(StockMedicine).filter(
        StockMedicine.medicine_id == medicine_id,
        StockMedicine.serial == serial
    ).first()


def get_stock(session, medicine_id, status):
    query = select(func.count()).where(
        (StockMedicine.medicine_id == medicine_id) &
        (StockMedicine.status == status)
    )
    return session.execute(query).scalar()