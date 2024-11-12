from fastapi import FastAPI
from routers import note, user

app = FastAPI()

app.include_router(note.router)
app.include_router(user.router)
@app.get("/")
async def welcome():
    return {"message": "Welcome to Notemanager"}