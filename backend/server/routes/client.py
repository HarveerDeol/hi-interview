from fastapi import APIRouter, HTTPException, status

from server.business.auth.auth_verifier import AuthVerifier
from server.business.auth.schema import UserTokenInfo
from server.business.client.get import get_client
from server.business.client.list import list_clients
from server.business.client.schema import PClient
from server.shared.databasemanager import DatabaseManager
from server.shared.pydantic import PList, BaseModel
from server.business.client.create import create_client


class PCreateClientRequest(BaseModel):
    email: str
    first_name: str
    last_name: str


def get_router(database: DatabaseManager, auth_verifier: AuthVerifier) -> APIRouter:
    router = APIRouter()

    @router.get("/client")
    async def list_clients_route(
        _: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PList[PClient]:
        with database.create_session() as session:
            clients = list_clients(session)
            return PList(data=clients)
        
    @router.post("/client", status_code=status.HTTP_201_CREATED)
    async def create_client_route(
        body: PCreateClientRequest,
        _: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PClient:
        with database.create_session() as session:
            return create_client(session, body.email, body.first_name, body.last_name)
        
    @router.get("/client/{client_id}")
    async def get_client_route(
        client_id: str,
        _: UserTokenInfo = auth_verifier.UserTokenInfo(),
    ) -> PClient:
        with database.create_session() as session:
            client = get_client(session, client_id)
            if client is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
            return client

    return router
