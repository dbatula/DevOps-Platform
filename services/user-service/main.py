from fastapi import Depends, FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from sqlalchemy.orm import Session # type: ignore

from database import SessionLocal, engine
from models import Base, UserDB

Base.metadata.create_all(bind=engine)

app = FastAPI()


class User(BaseModel):
    name: str
    email: str
    phone: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "user service is running"}


@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="user already exists")

    db_user = UserDB(name=user.name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "phone": db_user.phone,
    }


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
        }
        for user in users
    ]