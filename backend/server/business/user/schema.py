from datetime import datetime

from server.shared.pydantic import BaseModel


class PUser(BaseModel):
    id: str
    email: str
    password_hashed: str | None
    created_at: datetime
