from sqlalchemy import select

from server.business.auth.password import hash_password
from server.data.models.client import Client
from server.data.models.user import User
from server.shared.config import Config
from server.shared.databasemanager import DatabaseManager

TEST_USER_EMAIL = "admin@hi.com"
TEST_USER_PASSWORD = "password"

TEST_CLIENTS = [
    {"first_name": "Alice", "last_name": "Johnson", "email": "alice.johnson@example.com", "assigned": True},
    {"first_name": "Bob", "last_name": "Smith", "email": "bob.smith@example.com", "assigned": True},
    {"first_name": "Carol", "last_name": "Williams", "email": "carol.williams@example.com", "assigned": True},
    {"first_name": "David", "last_name": "Brown", "email": "david.brown@example.com", "assigned": False},
    {"first_name": "Emily", "last_name": "Davis", "email": "emily.davis@example.com", "assigned": False},
]


def main():
    config = Config.from_env()
    database = DatabaseManager.from_url(config.database_url)

    with database.create_session() as session:
        existing_user = session.execute(
            select(User).where(User.email == TEST_USER_EMAIL)
        ).scalars().one_or_none()

        if existing_user:
            print(f"User {TEST_USER_EMAIL} already exists, skipping user creation.")
            user_id = existing_user.id
        else:
            user = User(
                email=TEST_USER_EMAIL,
                password_hashed=hash_password(TEST_USER_PASSWORD),
            )
            session.add(user)
            session.flush()
            user_id = user.id
            print(f"Created user {TEST_USER_EMAIL} with password '{TEST_USER_PASSWORD}'")

        for test_client in TEST_CLIENTS:
            existing_client = session.execute(
                select(Client).where(Client.email == test_client["email"])
            ).scalars().one_or_none()

            if existing_client:
                print(f"Client {test_client['email']} already exists, skipping.")
                continue

            client = Client(
                email=test_client["email"],
                first_name=test_client["first_name"],
                last_name=test_client["last_name"],
                assigned_user_id=user_id if test_client["assigned"] else None,
            )
            session.add(client)
            assigned_label = f" (assigned to {TEST_USER_EMAIL})" if test_client["assigned"] else " (unassigned)"
            print(f"Created client {test_client['first_name']} {test_client['last_name']}{assigned_label}")

        session.commit()
        print("\nDone! You can log in with:")
        print(f"  Email:    {TEST_USER_EMAIL}")
        print(f"  Password: {TEST_USER_PASSWORD}")


if __name__ == "__main__":
    main()
