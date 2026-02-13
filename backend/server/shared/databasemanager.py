from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseManager:
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    def create_session(self) -> Session:
        return self.session_factory()

    @classmethod
    def from_url(cls, url: str) -> "DatabaseManager":
        return cls(create_engine(url))
