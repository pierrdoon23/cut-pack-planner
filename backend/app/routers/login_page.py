from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.schemas import LoginRequest, LoginResponse
from app.database import get_db
from app.crud import authenticate_user

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/ping")
async def ping():
    """
    Эндпоинт для проверки доступности сервера
    """
    return {"status": "ok", "message": "Server is running"} 

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    return LoginResponse(id=user.id, full_name=user.full_name, role=user.role)

@router.post("/", response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, full_name=user.full_name)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@router.patch("/{user_id}", response_model=schemas.UserSchema)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден")