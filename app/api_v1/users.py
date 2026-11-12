from fastapi import APIRouter
import bcrypt

from app.database import client as database
from app.schemas.users import RegisterUserRequest, RegisterUserResponse

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post('/register', response_model=RegisterUserResponse)
async def register(user: RegisterUserRequest) -> RegisterUserResponse:
    new_user = {
        "surname": user.surname,
        "name": user.name,
        "middle_name": user.middle_name,
        "nickname": user.nickname,
        "birthday": user.birthday, 
        "phone": user.phone,
        "password": bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    }
    response = (
        database.table("users")
        .insert(new_user)
        .execute()
    )

    return RegisterUserResponse(
        id=response.data[0].get('id'),
        surname=response.data[0].get('surname'),
        name=response.data[0].get('name'),
        middle_name=response.data[0].get('middle_name'),
        nickname=response.data[0].get('nickname'),
        birthday=response.data[0].get('birthday'),
        phone=response.data[0].get('phone')
    )

@router.post('/auth')
async def auth():
    return "PLACEHOLDER"