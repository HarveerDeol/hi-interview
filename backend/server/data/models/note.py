from typing import TYPE_CHECKING
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from server.data.models.base import Base

if TYPE_CHECKING:
    from server.data.models.client import Client
    from server.data.models.user import User


class Note(Base):
    __tablename__ = "note"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    client_id: Mapped[str] = mapped_column(String, ForeignKey("client.id"), nullable=False)
    created_by_user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    client: Mapped["Client"] = relationship("Client", foreign_keys=[client_id], back_populates="notes")
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_user_id])
