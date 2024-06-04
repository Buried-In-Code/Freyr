from sqlmodel import Session, SQLModel, create_engine

from freyr.constants import constants

connect_args = {"check_same_thread": False}
engine = create_engine(constants.settings.database.db_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
