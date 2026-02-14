from fastapi.testclient import TestClient

from server.data.models.client import Client
from server.data.models.note import Note
from server.shared.databasemanager import DatabaseManager


def test_list_notes(test_client: TestClient, database: DatabaseManager, user_id: str) -> None:
    with database.create_session() as session:
        client = Client(email="notes@example.com", first_name="Nathan", last_name="Patel")
        session.add(client)
        session.commit()
        client_id = client.id

        note1 = Note(client_id=client_id, created_by_user_id=user_id, content="First note")
        note2 = Note(client_id=client_id, created_by_user_id=user_id, content="Second note")
        session.add(note1)
        session.add(note2)
        session.commit()

    response = test_client.get(f"/client/{client_id}/note")
    assert response.status_code == 200

    data = response.json()
    assert len(data["data"]) == 2

    contents = [n["content"] for n in data["data"]]
    assert "First note" in contents
    assert "Second note" in contents

    for note in data["data"]:
        assert "id" in note
        assert note["client_id"] == client_id
        assert note["created_by_user_id"] == user_id
        assert "created_at" in note


def test_list_notes_empty(test_client: TestClient, database: DatabaseManager) -> None:
    with database.create_session() as session:
        client = Client(email="nonotes@example.com", first_name="Oliver", last_name="Quinn")
        session.add(client)
        session.commit()
        client_id = client.id

    response = test_client.get(f"/client/{client_id}/note")
    assert response.status_code == 200

    data = response.json()
    assert len(data["data"]) == 0


def test_list_notes_unauthenticated(unauthenticated_test_client: TestClient, database: DatabaseManager) -> None:
    with database.create_session() as session:
        client = Client(email="unauth-notes@example.com", first_name="Piper", last_name="Roberts")
        session.add(client)
        session.commit()
        client_id = client.id

    response = unauthenticated_test_client.get(f"/client/{client_id}/note")
    assert response.status_code == 401


def test_create_note(test_client: TestClient, database: DatabaseManager, user_id: str) -> None:
    with database.create_session() as session:
        client = Client(email="create-note@example.com", first_name="Quinn", last_name="Smith")
        session.add(client)
        session.commit()
        client_id = client.id

    response = test_client.post(
        f"/client/{client_id}/note",
        json={"content": "Important follow-up needed"},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["content"] == "Important follow-up needed"
    assert data["client_id"] == client_id
    assert data["created_by_user_id"] == user_id
    assert "id" in data
    assert "created_at" in data

    # Verify it was persisted
    response = test_client.get(f"/client/{client_id}/note")
    assert response.status_code == 200
    notes = response.json()["data"]
    assert len(notes) == 1
    assert notes[0]["content"] == "Important follow-up needed"


def test_create_note_nonexistent_client(test_client: TestClient) -> None:
    response = test_client.post(
        "/client/nonexistent-client-id/note",
        json={"content": "This should fail"},
    )
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data


def test_create_note_unauthenticated(unauthenticated_test_client: TestClient, database: DatabaseManager) -> None:
    with database.create_session() as session:
        client = Client(email="unauth-create@example.com", first_name="Rachel", last_name="Taylor")
        session.add(client)
        session.commit()
        client_id = client.id

    response = unauthenticated_test_client.post(
        f"/client/{client_id}/note",
        json={"content": "Unauthorized note"},
    )
    assert response.status_code == 401
