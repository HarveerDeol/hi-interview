from sqlalchemy.orm import Session

from server.business.client.schema import PClient
from server.data.models.client import Client


def create_client(session: Session, email: str, first_name: str, last_name: str) -> PClient:
    client = Client(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(client)
    session.commit()
    session.refresh(client)
    return PClient.model_validate(client)