import abc
import random
import string
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from common.config import HOST, PORT, USER, PWD, DB
from sqlalchemy.pool import NullPool

# For a production application, load this URL from an environment variable or config file.
# For example: from common.config import SQLALCHEMY_DATABASE_URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./my_database.db"

# SQLite only supports DEFERRED, IMMEDIATE, or EXCLUSIVE isolation levels.
# REPEATABLE READ is for PostgreSQL/MySQL and will raise an error.
_isolation_level = "DEFERRED"

# Use a null pool for SQLite, as it is a file-based database and doesn't
# require a connection pool for network connections.

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        SQLALCHEMY_DATABASE_URL,
        isolation_level=_isolation_level,
        poolclass=NullPool,  # Use NullPool, as it's a file-based DB
        # This is the most critical setting for SQLite with web frameworks.
        connect_args={"check_same_thread": False}
    )
)


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()

    @abc.abstractmethod
    def commit(self):
        self.session.commit()

    @abc.abstractmethod
    def rollback(self):
        self.session.rollback()
