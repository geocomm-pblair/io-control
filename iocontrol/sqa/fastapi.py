from iocontrol.sqa.engine import session_local


def session():
    """Database session dependency."""
    session_ = session_local()()
    try:
        yield session_
    finally:
        session_.close()
