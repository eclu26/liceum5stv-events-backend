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
    surname: str
    name: str
    middle_name: Optional[str]
    nickname: Optional[str]
    birthday: str
    phone: str

    model_config = {
        "from_attributes": True
    }