from datetime import date, datetime

from fastapi import FastAPI
from pydantic import BaseModel, constr

app = FastAPI()


class PatientSchema(BaseModel):
    """
   Schema for representing a patient.

   Attributes:
       id (int): Unique identifier for the patient.
       date_of_birth (date): The patient's date of birth.
       diagnoses (list[str]): List of diagnoses for the patient.
       created_at (datetime): Timestamp when the patient record was created.
       """
    id: int
    date_of_birth: date
    diagnosis: list[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    """
     Schema for representing a user.

     Attributes:
         username (str): The username of the user (3-30 characters).
         password (str): The password of the user (minimum 8 characters).
         role (str): The role of the user ('doctor', 'patient').
     """
    username: constr(min_length=3, max_length=30)
    password: constr(min_length=8)
    role: str

    class Config:
        from_attributes = True
