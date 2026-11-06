from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]] = []

    class Settings:
        name = "users"


class UserSignIn(BaseModel):
    email: EmailStr
    password: str