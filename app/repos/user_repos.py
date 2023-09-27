from sqlmodel import Session, select

from app.db import get_session, get_async_session
from app.usr_models import User


async def select_all_users():
    async with get_async_session() as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res

def find_user(name):
    with get_session() as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()