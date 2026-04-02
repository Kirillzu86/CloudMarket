from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
import secrets

import jwt


JWT_SECRET = os.getenv("CLOUDMARKET_JWT_SECRET", "cloudmarket-dev-secret-key-please-change-2026")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24


def hash_password(password: str, salt: str | None = None) -> str:
    salt_value = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_value.encode("utf-8"), 120000)
    return f"{salt_value}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, _ = password_hash.split("$", 1)
    except ValueError:
        return False

    expected = hash_password(password, salt)
    return hmac.compare_digest(expected, password_hash)


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {"sub": str(user_id), "exp": expires_at}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
