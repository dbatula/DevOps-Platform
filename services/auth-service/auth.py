import jwt # type: ignore
import datetime
from passlib.context import CryptContext # type: ignore

SECRET_KEY = "secret123"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)

def _safe_password(password: str) -> str:
    if password is None:
        return ""
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def hash_password(password: str):
    safe_password = _safe_password(password)
    return pwd_context.hash(safe_password)


def verify_password(password, hashed):
    safe_password = _safe_password(password)
    return pwd_context.verify(safe_password, hashed)


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")