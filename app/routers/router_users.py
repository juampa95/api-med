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
    hashed_pwd = auth_handler.get_password_hash(user.password)

    # Verificar si el usuario logueado es administrador o doctor
    if usr_log.is_admin:
        # El usuario logueado es administrador, puede crear un nuevo admin o doctor
        is_admin = user.is_admin
        is_doctor = user.is_doctor
    elif usr_log.is_doctor:
        # El usuario logueado es doctor, no puede crear ni admin ni doctor
        is_admin = False
        is_doctor = False
    else:
        # Otro caso, por ejemplo, si el usuario logueado no tiene un rol específico
        raise HTTPException(status_code=403, detail="Unauthorized")

    u = User(username=user.username, password=hashed_pwd, email=user.email,
             is_doctor=is_doctor, is_admin=is_admin)
    session.add(u)
    session.commit()
    response_content = {"message": "User registered successfully"}
    return JSONResponse(status_code=HTTP_201_CREATED, content=response_content)

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
