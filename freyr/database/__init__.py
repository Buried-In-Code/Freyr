__all__ = ["sqlite_filepath"]

from freyr import get_data_root
from freyr.database.tables import db
from freyr.settings import Settings

sqlite_filepath = get_data_root() / Settings().database.name
db.bind(
    provider="sqlite",
    filename=str(sqlite_filepath),
    create_db=True,
)
db.generate_mapping(create_tables=True)


@db.on_connect(provider="sqlite")
def sqlite_case_sensitivity(database, connection) -> None:  # noqa: ANN001, ARG001
    cursor = connection.cursor()
    cursor.execute("PRAGMA case_sensitive_like = OFF")
