from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la URL de conexión de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Función para obtener una sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session
