from fastapi import APIRouter, HTTPException, status

from server.business.auth.auth_verifier import AuthVerifier
from server.business.auth.schema import UserTokenInfo
from server.business.note.list import list_notes
from server.business.note.create import create_note
from server.business.client.get import get_client
from server.business.client.schema import PNote
from server.shared.databasemanager import DatabaseManager
from server.shared.pydantic import PList, BaseModel


class CreateNoteRequest(BaseModel):
    content: str


def get_router(database: DatabaseManager, auth_verifier: AuthVerifier) -> APIRouter:
    router = APIRouter()

    @router.get("/client/{client_id}/note")
    async def list_notes_route(
        client_id: str,
        _: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PList[PNote]:
        with database.create_session() as session:
            notes = list_notes(session, client_id)
            return PList(data=notes)

    @router.post("/client/{client_id}/note", status_code=status.HTTP_201_CREATED)
    async def create_note_route(
        client_id: str,
        request: CreateNoteRequest,
        user: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PNote:
        with database.create_session() as session:
            client = get_client(session, client_id)
            if client is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
                )

            note = create_note(session, client_id, user.user_id, request.content)
            return note

    return router
