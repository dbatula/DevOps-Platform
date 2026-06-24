from fastapi import FastAPI, Depends, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from sqlalchemy.orm import Session # type: ignore

from database import SessionLocal, engine
from models import Base, UserDB
from auth import hash_password, verify_password, create_token

app = FastAPI()

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "auth service is running"}


@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="user already exists")

    hashed = hash_password(user.password)

    db_user = UserDB(email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "user created"}


@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="wrong password")

    token = create_token({"email": user.email})

    return {"access_token": token}