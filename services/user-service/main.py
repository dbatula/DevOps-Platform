from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


class User(BaseModel):
    name: str
    email: str
    phone: str


@app.get("/")
def health():
    return {"status": "user service is running"}


@app.post("/users")
def create_user(user: User):

    user_id = len(users_db) + 1

    users_db[user_id] = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone
    }

    return users_db[user_id]


@app.get("/users/{user_id}")
def get_user(user_id: int):

    user = users_db.get(user_id)

    if not user:
        return {"error": "user not found"}

    return user


@app.get("/users")
def get_users():
    return list(users_db.values())