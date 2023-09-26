from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.usr_models import User, UserInput, UserLogin
from app.db import get_session
from app.auth.auth import AuthHandler
from starlette.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from starlette.responses import JSONResponse

router = APIRouter(prefix="/users")
auth_handler = AuthHandler()


@router.post('/registration', status_code=201, tags=['users'],
             description='Register new user')
async def register(user: UserInput, session: Session = Depends(get_session),
                   usr_log=Depends(auth_handler.get_current_user)):
    statement = select(User)
    users = session.exec(statement).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    hased_pwd = auth_handler.get_password_hash(user.password)

    # # Solo se permite a un administrador crear otro admin o doctores
    # # Un doctor no podria crear otro doctor o un admin
    # if usr_log.is_admin:
    #     is_doctor = User.is_doctor
    #     is_admin = User.is_admin
    # else:
    #     is_doctor = False
    #     is_admin = False
    # No funciona esta parte, no logro obtener los datos del usuario logueeado.


    u = User(username=user.username, password=hased_pwd, email=user.email,
             is_doctor=user.is_doctor, is_admin=user.is_admin)
    session.add(u)
    session.commit()
    return JSONResponse(status_code=HTTP_201_CREATED)

@router.post('/login',tags=['users'])
async def login(user: UserLogin, session: Session = Depends(get_session)):
    statement = select(User).where(User.username == user.username)
    user_found = session.exec(statement).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}
