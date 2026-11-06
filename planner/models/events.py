from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    # Поле создателя (почта пользователя)
    creator: Optional[EmailStr] = None

    class Settings:
        name = "events"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "Презентация книги по FastAPI",
                "tags": ["python", "fastapi", "mongodb"],
                "location": "Google Meet",
                "creator": "student@packt.com"
            }
        }


class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None