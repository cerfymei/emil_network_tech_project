from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

if TYPE_CHECKING:
    from models.users import User

# Таблица в БД
class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    location: str

    # ВНЕШНИЙ КЛЮЧ (Связь с таблицей user)
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: Optional["User"] = Relationship(back_populates="events")

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "title": "FastAPI Meetup",
                "image": "https://linktomyimage.com/image.png",
                "description": "Обсуждение практической работы №8",
                "tags": ["python", "fastapi", "sqlmodel"],
                "location": "Discord",
                "creator_id": 1
            }
        }

# Схема для обновления (все поля опциональны)
class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Новое название события",
                "location": "Главный корпус, ауд. 301"
            }
        }