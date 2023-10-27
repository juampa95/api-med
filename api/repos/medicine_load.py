import pandas as pd
import io


def validate_medicine(file):
    file_content = io.BytesIO(file.file.read())
    df = pd.read_excel(file_content).head(150)
    try:
        df = df.rename(columns={
            'TROQUEL': 'code',
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

    df = df[['code', 'name', 'drug', 'concentration', 'gtin']]
    df['code'] = df['code'].astype(int)
    df['gtin'] = (df['gtin']
                  .astype(str)
                  .str.rstrip('.0'))

    medicine_dict = df.to_dict(orient="records")

    return medicine_dict


# print(validate_medicine('data/ALFABETA COMPLETO.xlsx'))