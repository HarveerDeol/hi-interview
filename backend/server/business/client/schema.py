from datetime import datetime

from server.shared.pydantic import BaseModel


class PClient(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    assigned_user_id: str | None
    created_at: datetime
    updated_at: datetime


class PNote(BaseModel):
    id: str
    client_id: str
    created_by_user_id: str
    content: str
    created_at: datetime


# Include notes on the client model so API responses can return them
class PClientWithNotes(PClient):
    notes: list[PNote]
