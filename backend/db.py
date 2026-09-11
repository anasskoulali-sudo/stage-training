"""SQLModel engine and sessions. Does not drop tables."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import text
from sqlmodel import Session, create_engine

from backend.config import get_database_url

engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
)


def ensure_schema() -> None:
    """Add columns the app needs without dropping existing tables."""
    with engine.begin() as conn:
        exists = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = 'stage_site'
                  AND TABLE_NAME = 'users'
                  AND COLUMN_NAME = 'mot_de_passe_clair'
                """
            )
        ).scalar_one()
        if not exists:
            conn.execute(
                text(
                    """
                    ALTER TABLE stage_site.users
                    ADD COLUMN mot_de_passe_clair VARCHAR(255) NULL
                    AFTER mot_de_passe
                    """
                )
            )


@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
