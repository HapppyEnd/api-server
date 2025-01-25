from datetime import datetime, timezone

import bcrypt
from sqlalchemy import Column, create_engine, Date, DateTime, Integer, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import JSON

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """
     Dependency that provides a database session.

     This function yields a database session and ensures that the
     session is closed after use. It should be used as a dependency
     in FastAPI routes.

     Yields:
         Session: A SQLAlchemy session for database operations.
     """
    db = Session()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        password (str): Hashed password of the user.
        role (str): Role of the user (e.g., 'doctor', 'admin').

    Methods:
        set_password(password: str): Hashes and set the user's password.
        check_password(password: str) -> bool: Check if the provided
        password matches the hashed password.
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, index=True)

    def set_password(self, password: str):
        """Hashes and save the password."""
        self.password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Check if the password matches the stored hashed password.

        :param password: The password to check.
        :return: bool: True if the hashed password matches.
        """
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8"))


class Patient(Base):
    """
       SQLAlchemy model representing a patient.

       Attributes:
           id (int): Unique identifier for the patient.
           date_of_birth (date): The patient's date of birth.
           diagnoses (list): List of diagnoses for the patient.
           created_at (datetime): Timestamp when the patient record
           was created.
       """
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_of_birth = Column(Date, nullable=False)
    diagnoses = Column(MutableList.as_mutable(JSON))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


Base.metadata.create_all(engine)
