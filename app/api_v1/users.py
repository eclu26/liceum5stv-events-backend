from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from postgrest.exceptions import APIError
import bcrypt
import jwt

from app.settings import settings
from app.database import client as database
from app.schemas.users import *

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

security = HTTPBearer()

@router.post('/register', response_model=RegisterUserResponse)
async def register(req_user: RegisterUserRequest) -> RegisterUserResponse:
    user = {
        "surname": req_user.surname,
        "name": req_user.name,
        "middle_name": req_user.middle_name,
        "nickname": req_user.nickname,
        "birthday": req_user.birthday, 
        "phone": req_user.phone,
        "password": bcrypt.hashpw(req_user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    }

    try:
        response = (
            database.table("users")
            .insert(user)
            .execute()
        )
    except APIError:
        raise HTTPException(
            status_code=409
        )

    return RegisterUserResponse(
        id=response.data[0].get('id'),
        is_admin=response.data[0].get('is_admin')
    )

@router.post('/auth', response_model=AuthUserResponse)
async def auth(req_user: AuthUserRequest) -> AuthUserResponse:
    response = (
        database.table("users")
        .select("*")
        .eq("phone", req_user.phone)
        .execute()
    )

    if len(response.data) < 1:
        raise HTTPException(
            status_code=404
        )
    else:
        user = response.data[0]

    if not bcrypt.checkpw(req_user.password.encode('utf-8'), user.get('password').encode('utf-8')):
        raise HTTPException(
            status_code=401
        )

    payload = {
        "sub": user.get('id'),
        "is_admin": user.get('is_admin'),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_time)
    }

    token = jwt.encode(payload, settings.jwt_key, algorithm=settings.jwt_algorithm)

    return AuthUserResponse(
        jwt=token
    )

@router.post('/check-logged-user', response_model=CheckLoggedUserResponse)
async def check_logged_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> CheckLoggedUserResponse:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.jwt_key, algorithms=settings.jwt_algorithm)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401
        )

    response = (
        database.table("users")
        .select("*")
        .eq("id", payload.get('sub'))
        .execute()
    )

    if len(response.data) < 1:
        raise HTTPException(
            status_code=404
        )

    return CheckLoggedUserResponse(
        id=response.data[0].get('id'),
        is_admin=response.data[0].get('is_admin'),
        surname=response.data[0].get('surname'),
        name=response.data[0].get('name'),
        middle_name=response.data[0].get('middle_name'),
        nickname=response.data[0].get('nickname'),
        birthday=response.data[0].get('birthday'),
        phone=response.data[0].get('phone')
    )