from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    events: Optional[List[Event]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@packt.com",
                "password": "StrongPassword123!",
                "username": "StudentUser",
                "events": []
            }
        }


# Модель для входа в систему (нужен только email и пароль)
class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@packt.com",
                "password": "StrongPassword123!"
            }
        }