from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

from app.database import enable_sqlite_foreign_keys


def test_sqlite_foreign_keys_are_enabled():
    assert event.contains(Engine, "connect", enable_sqlite_foreign_keys)

    engine = create_engine("sqlite://")
    with engine.connect() as connection:
        enabled = connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one()

    assert enabled == 1
