from datetime import date, datetime
from fastapi import FastAPI
from pydantic import BaseModel, constr

app = FastAPI()


class Patient(BaseModel):
    id: int
    date_of_birth: date
    diagnoses: list[str]
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    username: constr(min_length=3, max_length=30)
    password: constr(min_length=8)
    role: str

    class Config:
        orm_mode = True
