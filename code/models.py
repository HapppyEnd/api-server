from datetime import datetime, timezone

import bcrypt
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.types import JSON

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, index=True, default='patient')

    def set_password(self, password: str):
        """Save hashed password."""
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check hashed password."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8'))


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_of_birth = Column(Date, nullable=False)
    # Используем MutableDict для поддержки изменений
    diagnosis = Column(MutableDict.as_mutable(JSON), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
