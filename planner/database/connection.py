from sqlmodel import SQLModel, Session, create_engine
import os

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"

connect_args = {"check_same_thread": False}
engine_url = create_engine(
    database_connection_string, 
    echo=True, 
    connect_args=connect_args
)

def conn():
    """Создание всех таблиц при запуске приложения"""
    SQLModel.metadata.create_all(engine_url)

def get_session():
    """Внедрение зависимости сессии в эндпоинты"""
    with Session(engine_url) as session:
        yield session