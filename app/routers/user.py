from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from sqlalchemy.future import select
from backend.db import Base
from typing import List, Annotated
from models import User, Note
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, update, delete
from slugify import slugify

# Создаем роутер с префиксом "/user" и тегом "user" для группировки связанных маршрутов
router = APIRouter(prefix="/user", tags=["user"])


def generate_unique_slug(username: str, db: Session) -> str:
    # Генерация уникального slug.
    base_slug = slugify(username)
    unique_slug = base_slug
    counter = 1
    # Проверка на существование slug в базе
    while db.execute(select(User).where(User.slug == unique_slug)).scalars().first():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    return unique_slug


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


# Получаем всех пользователей из базы данных.
# Параметры:
# - db (Session): Объект для работы с базой данных.
# Возвращает:
# - List[User]: Список всех пользователей.

@router.get("/user/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    return user


# Функция для получения пользователя по ID
# Получаем пользователя из базы данных по его идентификатору.
# Параметры:
# - user_id (int): Идентификатор пользователя, которого нужно получить.
# - db (Session): Объект для работы с базой данных.
# Возвращает:
# - User: Пользователь с указанным идентификатором, если он найден.
# - HTTPException: Исключение, если пользователь не найден (404).


@router.get("/{user_id}/notes")
async def notes_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    notes = db.scalars(select(Note).where(Note.user_id == user_id)).all()
    return notes


# Функция для получения заметок пользователя по его ID
# Получаем список заметок для пользователя по его идентификатору.
# Параметры:
# - user_id (int): Идентификатор пользователя, чьи заметки нужно получить.
# - db (Session): Объект для работы с базой данных.
# Возвращает:
# - List[Note]: Список заметок, принадлежащих указанному пользователю.


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], user: CreateUser):
    existing_user = db.execute(select(User).where(User.username == user.username)).scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")

    db.execute(insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username)
    ))

    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# Функция для создания нового пользователя
# Создание нового пользователя в системе.
# Параметры:
# - db (Session): Объект для работы с базой данных.
# - user (CreateUser): Данные для создания нового пользователя, содержащие имя пользователя, имя, фамилию и возраст.
# Возвращает:
# - dict: Словарь с кодом состояния и сообщением о результате транзакции.

@router.put("/update/{user_id}")
async def update_user(
        user_id: int,
        user: UpdateUser,
        db: Annotated[Session, Depends(get_db)]
):
    existing_user = db.scalar(select(User).where(User.id == user_id))

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    db.execute(update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.firstname)
    ))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


# Роутер для работы с базой данных
# Обновление данных существующего пользователя.
# Параметры:
# - user_id (int): ID пользователя, чьи данные необходимо обновить.
# - user (UpdateUser): Объект с новыми данными для пользователя, такими как имя, фамилия и возраст.
# - db (Session): Объект для работы с базой данных.
# Возвращает:
# - dict: Словарь с кодом состояния и сообщением о результате обновления.


@router.delete("/delete")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where(User.id == user_id))
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

    # Удаление всех заметок связанных с пользователем
    db.execute(delete(Note).where(Note.user_id == user_id))

    # Удаление пользователя
    db.execute(delete(User).where(User.id == user_id))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User and associated notes were successfully deleted'
    }

# Роутер для работы с базой данных
# Удаление существующего пользователя и его заметок из системы.
# Параметры:
# - user_id (int): ID пользователя, которого необходимо удалить.
# - db (Session): Объект для работы с базой данных.
# Возвращает:
# - dict: Словарь с кодом состояния и сообщением о результате удаления.
