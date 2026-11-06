from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from database.connection import get_session
from models.events import Event, EventUpdate
from models.users import User
from typing import List, Sequence

event_router = APIRouter(tags=["Events"])

# CREATE
@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(new_event: Event, session: Session = Depends(get_session)) -> dict:
    # Если передан creator_id, проверяем, существует ли такой пользователь
    if new_event.creator_id:
        creator = session.get(User, new_event.creator_id)
        if not creator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {new_event.creator_id} does not exist"
            )
            
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {
        "message": "Event created successfully",
        "id": new_event.id
    }

# READ ALL
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> Sequence[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events

# READ ONE
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event

# UPDATE (Исправлено)
@event_router.put("/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    
    # Берем только те поля, которые действительно переданы в запросе
    update_dict = new_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(event, key, value)
        
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

# DELETE
@event_router.delete("/{id}")
async def delete_event(id: int, session: Session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    session.delete(event)
    session.commit()
    return {"message": "Event deleted successfully."}