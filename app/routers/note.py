from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from sqlalchemy.future import select
from models import Note, User
from schemas import CreateNote, UpdateNote
from sqlalchemy import insert, update, delete
from typing import Annotated, List
from slugify import slugify

# Создаем роутер с префиксом "/note" и тегом "note" для группировки связанных маршрутов
router = APIRouter(prefix="/note", tags=["note"])


@router.get("/")
async def all_notes(db: Annotated[Session, Depends(get_db)]):
    notes = db.scalars(select(Note)).all()
    return notes

# Получаем все заметки из базы данных.
# Параметры:
# - db: Session - объект для работы с базой данных.
# Возвращает:
# - List[Note] - список всех заметок.

@router.get("/note/{note_id}")
async def note_by_id(note_id: int, db: Annotated[Session, Depends(get_db)]):
    note = db.execute(select(Note).where(Note.id == note_id)).scalars().first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note was not found")
    return note

# Извлекаем запись заметки по note_id.
# Параметры:
# - note_id: int - идентификатор заметки.
# - db: Session - объект для работы с базой данных.
# Возвращает:
# - Note - найденная заметка.
# Генерирует:
# - HTTPException - 404, если заметка не найдена.

@router.post("/create")
async def create_note(
        user_id: int,
        db: Annotated[Session, Depends(get_db)],
        note: CreateNote
):
    # Проверка на существующего пользователя
    existing_user = db.execute(select(User).where(User.id == user_id)).scalars().first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    # Создание заметки
    db.execute(insert(Note).values(
        title=note.title,
        content=note.content,
        priority=note.priority,
        user_id=user_id,  # Устанавливаем связь с пользователем
        slug=slugify(note.title)  # Генерируем slug на основе заголовка заметки
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

# Создание новой заметки.
# Параметры:
# - user_id: int - идентификатор пользователя, который создает заметку.
# - db: Session - объект для работы с базой данных.
# - note: CreateNote - данные заметки для создания.
# Возвращает:
# - dict - статус создания заметки.
# Генерирует:
# - HTTPException - 404, если пользователь не найден.

@router.put("/update/{note_id}")
async def update_note(
        note_id: int, note: UpdateNote,
        db: Annotated[Session, Depends(get_db)]):


    existing_note = db.scalar(select(Note).where(Note.id == note_id))
if existing_note is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note was not found"
    )

db.execute(update(Note).where(Note.id == note_id).values(
    title=note.title,
    content=note.content,
    priority=note.priority,
    slug=slugify(note.title)
))
db.commit()

return {
    'status_code': status.HTTP_200_OK,
    'transaction': 'Note update is successful!'
}


# Обновление существующей заметки.
# Параметры:
# - note_id: int - идентификатор заметки для обновления.
# - note: UpdateNote - данные для обновления заметки.
# - db: Session - объект для работы с базой данных.
# Возвращает:
# - dict - статус обновления заметки.
# Генерирует:
# - HTTPException - 404, если заметка не найдена.


@router.delete("/delete")
async def delete_note(
        note_id: int,
        db: Annotated[Session, Depends(get_db)]
):


# Проверка на существующую заметку
existing_note = db.scalar(select(Note).where(Note.id == note_id))
if existing_note is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note was not found"
    )

# Удаление заметки
db.execute(delete(Note).where(Note.id == note_id))
db.commit()

return {
    'status_code': status.HTTP_200_OK,
    'transaction': 'Note was successfully deleted'
}

# Удаление заметки по note_id.
# Параметры:
# - note_id: int - идентификатор заметки для удаления.
# - db: Session - объект для работы с базой данных.
# Возвращает:
# - dict - статус удаления заметки.
# Генерирует:
# - HTTPException - 404, если заметка не найдена.
