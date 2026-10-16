from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form

class Todo(BaseModel):
    id: Optional[int] = None
    item: str

    @classmethod
    def as_form(cls, item: str = Form(...)):
            return cls(item=item)


    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "item": "Пример задачи"
            }
        }

class TodoItem(BaseModel):
    item: str

    class Config:
        json_schema_extra = {
            "example": {
                "item": "Обновленный текст задачи"
            }
        }

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        json_schema_extra = {
            "example": {
                "todos": [
                    {"item": "Первая задача"},
                    {"item": "Вторая задача"}
                ]
            }
        }