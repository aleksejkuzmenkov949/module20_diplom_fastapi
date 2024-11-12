1. проект "API для системы управления заметками пользователей."

основные маршруты в API-роутерах :

1)роутер note

get '/' с функцией all_notes.
get '/note_id' с функцией note_by_id.
post '/create' с функцией create_note.
put '/update' с функцией update_note.
delete '/delete' с функцией delete_note.

2)роутер user

get '/' с функцией all_users.
get '/user_id' с функцией user_by_id.
post '/create' с функцией create_user.
put '/update' с функцией update_user.
delete '/delete' с функцией delete_user.



2..запуск приложения командой в терминале :uvicorn main:app --reload

3.. требования к проекту , также прописаны в файле requirements.txt :
alembic==1.14.0
annotated-types==0.7.0
anyio==4.6.2.post1
click==8.1.7
colorama==0.4.6
exceptiongroup==1.2.2
fastapi==0.115.4
greenlet==3.1.1
h11==0.14.0
idna==3.10
Jinja2==3.1.4
Mako==1.3.6
MarkupSafe==3.0.2
pydantic==2.9.2
pydantic_core==2.23.4
python-multipart==0.0.17
slugify==0.0.1
sniffio==1.3.1
SQLAlchemy==2.0.36
starlette==0.41.2
typing_extensions==4.12.2
uvicorn==0.32.0

4. создание базы данных приложжения через  команду инициализации миграции :alembic revision --autogenerate -m "Initial migration"


5. ссылка для запуска приложения :  http://127.0.0.1:8000

студент Кузьменков Алексей

