from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn
from typing import List

user_router = APIRouter(tags=["User"])
user_database = Database(User)


# 1. READ: Получить список всех пользователей
@user_router.get("/", response_model=List[User])
async def retrieve_all_users() -> List[User]:
    users = await user_database.get_all()
    return users


# 2. READ: Получить конкретного пользователя по ID
@user_router.get("/{id}", response_model=User)
async def retrieve_user(id: PydanticObjectId) -> User:
    user = await user_database.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с указанным ID не найден!"
        )
    return user


# 3. CREATE: Регистрация нового пользователя
@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже зарегистрирован!"
        )
    await user_database.save(user)
    return {"message": "Пользователь успешно зарегистрирован в MongoDB!"}


# 4. Вход пользователя (авторизация)
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким email не существует!"
        )
    if user_exist.password == user.password:
        return {"message": "Вход выполнен успешно!"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный пароль!"
    )