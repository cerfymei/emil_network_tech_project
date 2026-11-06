from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.events import Event, EventUpdate
from models.users import User
from typing import List
from beanie import PydanticObjectId, WriteRules

event_router = APIRouter(tags=["Events"])
event_database = Database(Event)


# 1. READ: Получить все события
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


# 2. READ: Получить событие по его ObjectId
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие с указанным ID не найдено!"
        )
    return event


# 3. CREATE: Создать событие и привязать его к пользователю в MongoDB
@event_router.post("/new")
async def create_event(body: Event) -> dict:
    # Сохраняем событие в коллекцию events
    await event_database.save(body)

    # Если указан автор, находим его в базе и добавляем событие в его список
    if body.creator:
        user = await User.find_one(User.email == body.creator)
        if user:
            if user.events is None:
                user.events = []
            user.events.append(body)
            await user.save(link_rule=WriteRules.WRITE)

    return {"message": "Событие успешно создано и привязано к пользователю!"}


# 4. UPDATE: Обновить параметры события
@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие для обновления не найдено!"
        )
    return updated_event


# 5. DELETE: Удалить событие по ID
@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие для удаления не найдено!"
        )
    return {"message": "Событие успешно удалено из MongoDB!"}