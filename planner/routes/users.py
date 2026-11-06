from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from database.connection import get_session
from models.users import User, UserSignIn, UserPublic
from typing import List

user_router = APIRouter(tags=["User"])

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_user_up(user: User, session: Session = Depends(get_session)) -> dict:
    # Проверка на существование пользователя
    statement = select(User).where(User.email == user.email)
    user_exist = session.exec(statement).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created successfully", "user_id": user.id}

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, session: Session = Depends(get_session)) -> dict:
    statement = select(User).where(User.email == user.email)
    user_exist = session.exec(statement).first()
    if not user_exist or user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid details passed."
        )
    return {"message": "User signed in successfully."}

@user_router.get("/{id}")
async def get_user_with_events(id: int, session: Session = Depends(get_session)):
    """Показывает пользователя и список его событий (демонстрация связи 1:N)"""
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Возвращаем пользователя и его связанные события
    return {
        "id": user.id,
        "email": user.email,
        "events": user.events
    }