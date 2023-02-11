from .session import SessionLocal


def get_db():
    """A helper function to access the database when required, and close when done"""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
