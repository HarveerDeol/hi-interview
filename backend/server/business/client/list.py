from sqlalchemy import select
from sqlalchemy.orm import Session

from server.business.client.schema import PClient
from server.data.models.client import Client


def list_clients(session: Session) -> list[PClient]:
    clients = session.execute(select(Client)).scalars().all()
    return [PClient.model_validate(client) for client in clients]
