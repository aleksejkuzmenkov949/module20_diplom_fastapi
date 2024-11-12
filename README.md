module20_diplom_fastapi/
│
├── .venv/
│
├── app/
│   ├── backend/
│   │   ├── db.py
│   │   └── db_depends.py
│   │
│   ├── migrations/
│   │   └── versions/
│   │       ├── env.py
│   │       ├── README
│   │       └── script.py.mako
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── note.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── note.py
│   │   └── user.py
│   │
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
│
├── alembic.ini
├── notemanager.db
├── readme.txt
└── requirements.txt

app/
- backend/: Содержит файлы, отвечающие за взаимодействие с базой данных.
 - db.py: Модуль для конфигурации базы данных.
 - db_depends.py: Файл для установки зависимостей баз данных. 
- migrations/: Содержит файлы и папки для миграции базы данных
-models/: Определяет структуры данных (модели) для приложения. 
- note.py: Определяет модель для заметок.
 - user.py: Определяет модель для пользователей.
 - routers/: Определяет маршруты и обработчики API. - *
- note.py: Обработчик маршрутов для работы со заметками. 
- user.py: Обработчик маршрутов для работы с пользователями. 
-main.py: Основной файл приложения, запускающий сервер и содержащий основные настройки. – 
-schemas.py: Определяет схемы  данных, используемых в API.
