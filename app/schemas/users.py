from typing import Optional
from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    surname: str
    name: str
    middle_name: Optional[str]
    nickname: Optional[str]
    birthday: str
    phone: str
    password: str

class RegisterUserResponse(BaseModel):
    id: str
    is_admin: bool

    model_config = {
        "from_attributes": True
    }

class AuthUserRequest(BaseModel):
    phone: str
    password: str

class AuthUserResponse(BaseModel):
    jwt: str

    model_config = {
        "from_attributes": True
    }

class CheckLoggedUserRequest(BaseModel):
    jwt: str

class CheckLoggedUserResponse(BaseModel):
    id: str
    is_admin: bool
    surname: str
    name: str
    middle_name: Optional[str]
    nickname: Optional[str]
    birthday: str
    phone: str

    model_config = {
        "from_attributes": True
    }