from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from models.events import Event

# Таблица в БД
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str

    # Связь 1:N — один пользователь имеет много событий
    events: List["Event"] = Relationship(back_populates="creator")

# Схема для авторизации
class UserSignIn(BaseModel):
    email: str
    password: str

# Схема ответа без пароля (для безопасности в Swagger)
class UserPublic(BaseModel):
    id: int
    email: str