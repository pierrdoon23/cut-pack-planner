from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.db.database import SessionLocal
from app.crud import crud

router = APIRouter(prefix="/todos", tags=["Todos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo, user_id)

@router.get("/user/{user_id}", response_model=list[schemas.TodoOut])
def get_user_todos(user_id: int, db: Session = Depends(get_db)):
    return crud.get_todos_for_user(db, user_id)
