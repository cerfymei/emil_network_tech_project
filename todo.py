from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()
todo_list = []

# 1. CREATE: Добавление задачи (возвращает статус 201 Created)
@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Задача успешно добавлена"}

# 2. READ: Получение всех задач с использованием response_model
@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> dict:
    return {"todos": todo_list}

# 3. READ: Получение одной задачи по ID с обработкой 404
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="ID задачи")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка: задача с таким ID не найдена"
    )

# 4. UPDATE: Обновление текста задачи по ID
@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="ID обновляемой задачи")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {"message": "Задача успешно обновлена"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка обновления: задача с таким ID не существует"
    )

# 5. DELETE: Удаление одной задачи по ID
@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int = Path(..., title="ID задачи")) -> dict:
    for index in range(len(todo_list)):
        if todo_list[index].id == todo_id:
            todo_list.pop(index)
            return {"message": "Задача успешно удалена"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка удаления: задача с указанным ID не найдена"
    )

# 6. DELETE: Очистка всех задач
@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {"message": "Все задачи успешно очищены"}