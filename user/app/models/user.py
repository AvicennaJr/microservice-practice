from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.db.base import Base


class User(Base):
    """Define the structure of 'users' table"""

    __tablename__ = "users"  # name of the table in postgres database

    id = Column(
        Integer, primary_key=True, index=True
    )  # primary key paramter will make the id column auto-increment
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
