from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.usr_models import User, UserInput, UserLogin, ChangePwd
from app.db import get_session
from app.auth.auth import AuthHandler
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from starlette.responses import JSONResponse
from app.repos.auth_repos import check_access

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

    # Permisos para crear usuarios según nivel de acceso

    if check_access(usr_log, ['ADMIN']):
        access_level = user.access_level
    elif check_access(usr_log, ['DOCTOR']):
        if user.access_level not in ['ADMIN', 'DOCTOR']:
            access_level = user.access_level
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")
    elif check_access(usr_log, ['NURSE']):
        if user.access_level in ['USER', 'PATIENT']:
            access_level = user.access_level
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

    u = User(username=user.username, password=hashed_pwd, email=user.email,
             access_level=access_level)
    session.add(u)
    session.commit()
    response_content = {"message": "User registered successfully"}
    return JSONResponse(status_code=HTTP_201_CREATED, content=response_content)


@router.post('/login', tags=['users'])
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


@router.post('/changePwd', tags=['users'])
async def changepassword(pwd: ChangePwd, session: Session = Depends(get_session),
                         usr_log=Depends(auth_handler.get_current_user)):
    if not auth_handler.verify_password(pwd.password, usr_log.password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    hashed_pwd = auth_handler.get_password_hash(pwd.newpassword)
    usr_log.password = hashed_pwd
    session.commit()

    return {"message": "Contraseña cambiada exitosamente"}
