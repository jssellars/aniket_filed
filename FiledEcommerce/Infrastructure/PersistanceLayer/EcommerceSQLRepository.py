from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy.orm import Session

from FiledEcommerce.Api.startup import fixtures


@contextmanager
def session_scope() -> ContextManager[Session]:
    """
    Context manager to gracefully handle sessions

    Copied from documentation
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """
    session = fixtures.sql_db_session()

    try:
        yield session
        # The objects within the session are expired upon commit,
        # set expire_on_commit to false to keep using them
        session.expire_on_commit = False
        session.commit()

    # intentional wide scope to rollback session
    except:
        session.rollback()
        raise
    finally:
        session.close()
