__all__ = []


from freyr import get_data
from freyr.constants import constants
from freyr.database.tables import db
from freyr.settings import Source

if constants.settings.database.source == Source.POSTGRES:
    db.bind(
        provider="postgres",
        user=constants.settings.database.user,
        password=constants.settings.database.password,
        host=constants.settings.database.host,
        database=constants.settings.database.name,
    )
else:
    filepath = get_data() / constants.settings.database.name
    db.bind(provider="sqlite", filename=str(filepath), create_db=True)
db.generate_mapping(create_tables=True)


@db.on_connect(provider="sqlite")
def sqlite_case_sensitivity(database, connection) -> None:  # noqa: ANN001, ARG001
    cursor = connection.cursor()
    cursor.execute("PRAGMA case_sensitive_like = OFF")
