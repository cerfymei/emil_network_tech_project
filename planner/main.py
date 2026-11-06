from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqladmin import Admin, ModelView

from database.connection import conn, engine_url
from routes.users import user_router
from routes.events import event_router
from models.users import User
from models.events import Event
import uvicorn

app = FastAPI(title="Event Planner API")

# Регистрация маршрутов
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# ================= НАСТРОЙКА АДМИНКИ =================
admin = Admin(app, engine_url, title="Панель администратора")

class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    # Какие колонки показывать в таблице
    column_list = [User.id, User.email, User.events]
    column_searchable_list = [User.email]

class EventAdmin(ModelView, model=Event):
    name = "Событие"
    name_plural = "События"
    icon = "fa-solid fa-calendar"
    # Показываем поля и связанного создателя
    column_list = [Event.id, Event.title, Event.location, Event.creator]
    column_searchable_list = [Event.title, Event.location]

admin.add_view(UserAdmin)
admin.add_view(EventAdmin)
# =====================================================

@app.on_event("startup")
def on_startup():
    conn()

@app.get("/")
async def home():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)