from fastapi import HTTPException
from typing import List


def verify_access2(user, required_permissions):
    """Funcion que verifica que el usuario contenga alguno de los permisos incluidos
    en la lista required_permissions. Utilizada para dar acceso a los diferentes
    endpoints solo a aquellos usuarios con nivel de acceso autorizado"""
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    if not any(getattr(user, perm, False) for perm in required_permissions):
        raise HTTPException(status_code=403, detail='Forbidden')


def verify_access(user, required_permissions: List[str]):
    """Funcion que verifica que el usuario contenga alguno de los permisos incluidos
    en la lista required_permissions. Utilizada para dar acceso a los diferentes
    endpoints solo a aquellos usuarios con nivel de acceso autorizado"""
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    if user.access_level not in required_permissions:
        raise HTTPException(status_code=403, detail='Forbidden')


def check_access(user, required_permissions: List[str]):
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    if user.access_level in required_permissions:
        return True
    else:
        return False