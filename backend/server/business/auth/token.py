from datetime import datetime, timedelta, timezone

import jwt

from server.shared.config import Config

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(config: Config, user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, config.access_token_secret_key, algorithm="HS256")
