from sqlmodel import Session, select

from app.db import get_session
from app.usr_models import User

def find_user(name):
    with get_session() as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
