from datetime import date, datetime
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Patient(BaseModel):
    id: int
    date_of_birth: date
    diagnoses: list[str]
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    password: str
    role: str