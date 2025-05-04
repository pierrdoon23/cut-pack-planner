from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import user_router, todo_router

app = FastAPI(title="ToDo List API")

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Подключение роутеров
app.include_router(user_router)
app.include_router(todo_router)
