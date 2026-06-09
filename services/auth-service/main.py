from fastapi import FastAPI
from pydantic import BaseModel
from auth import hash_password, verify_password, create_token

app = FastAPI()

fake_db = {}

class User(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(user: User):
    if user.email in fake_db:
        return {"error": "user already exists"}

    hashed = hash_password(user.password)
    fake_db[user.email] = hashed

    return {"message": "user created"}

@app.post("/login")
def login(user: User):
    stored_password = fake_db.get(user.email)

    if not stored_password:
        return {"error": "user not found"}

    if not verify_password(user.password, stored_password):
        return {"error": "wrong password"}

    token = create_token({"email": user.email})

    return {"access_token": token}
