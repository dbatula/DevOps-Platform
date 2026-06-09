import jwt # type: ignore
import datetime
from passlib.context import CryptContext # type: ignore

SECRET_KEY = "secret123"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"

)

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")