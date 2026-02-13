from fastapi import APIRouter
from server.shared.pydantic import BaseModel, Field
from sqlalchemy import select

from server.shared.config import Config
from server.shared.databasemanager import DatabaseManager


class PingResponse(BaseModel):
    healthy: str = Field(...)


def get_router(_: Config, database: DatabaseManager) -> APIRouter:
    router = APIRouter()

    @router.get("/ping")
    async def ping() -> PingResponse:
        with database.create_session() as session:
            session.execute(select(1)).all()
            return PingResponse(healthy="true")

    return router
