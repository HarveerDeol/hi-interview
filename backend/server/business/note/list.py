from sqlalchemy import select
from sqlalchemy.orm import Session

from server.business.client.schema import PNote
from server.data.models.note import Note


def list_notes(session: Session, client_id: str) -> list[PNote]:
    notes = session.execute(
        select(Note)
        .where(Note.client_id == client_id)
        .order_by(Note.created_at.desc())
    ).scalars().all()
    
    return [PNote.model_validate(note) for note in notes]
