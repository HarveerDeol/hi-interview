from fastapi import APIRouter, HTTPException

from server.business.auth.auth_verifier import AuthVerifier
from server.business.auth.schema import UserTokenInfo
from server.business.client.get import get_client
from server.business.client.schema import PNote
from server.business.note.create import create_note
from server.business.note.list import list_notes
from server.shared.databasemanager import DatabaseManager
from server.shared.pydantic import PList
from server.shared.pydantic import BaseModel


class PCreateNoteRequest(BaseModel):
    content: str


def get_router(database: DatabaseManager, auth_verifier: AuthVerifier) -> APIRouter:
    router = APIRouter()

    @router.get("/client/{client_id}/note")
    async def list_notes_route(
        client_id: str,
        current_user: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PList[PNote]:
        with database.create_session() as session:
            if get_client(session, client_id) is None:
                raise HTTPException(status_code=404, detail="Client not found")
            notes = list_notes(session, client_id)
            return PList(data=notes)

    @router.post("/client/{client_id}/note")
    async def create_note_route(
        client_id: str,
        body: PCreateNoteRequest,
        current_user: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PNote:
        with database.create_session() as session:
            if get_client(session, client_id) is None:
                raise HTTPException(status_code=404, detail="Client not found")
            note = create_note(session, client_id, current_user.id, body.content)
            return note

    return router