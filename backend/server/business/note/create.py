from sqlalchemy.orm import Session

from server.business.client.schema import PNote
from server.data.models.note import Note


def create_note(session: Session, client_id: str, user_id: str, content: str) -> PNote:
    note = Note(
        client_id=client_id,
        created_by_user_id=user_id,
        content=content,
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return PNote.model_validate(note)