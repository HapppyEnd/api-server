from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import JSON

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_of_birth = Column(Date, nullable=False)
    # Используем MutableDict для поддержки изменений
    diagnosis = Column(MutableDict.as_mutable(JSON), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
