import datetime
import os
import jwt
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import Patient, User, get_db
from passlib.context import CryptContext
from schemas import PatientSchema, UserSchema
from sqlalchemy.orm import Session

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    """
     Creates a JWT token with the given data and expiration time.

     :param data: Data to be encoded in the token.
     :param expires_delta: Expiration time for the token.
     If not provided, the default value is used.
     :return: Encoded JWT token.
     """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(
            datetime.timezone.utc) + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/login")
def login(
        username: str = Body(...),
        password: str = Body(...),
        db: Session = Depends(get_db)
):
    """
       User login. Validates credentials and creates a JWT token for
       authorization.

       :param username: Username for login.
       :param password: Password for login.
       :param db: Database session.
       :raises HTTPException: If the credentials are invalid.
       :return: A dictionary with the access token and token type.
       """
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(
        data={"username": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/patients", response_model=list[PatientSchema])
def read_patients(token: str = Depends(oauth2_scheme),
                  db: Session = Depends(get_db)):
    """
      Retrieves a list of patients.
      Accessible only to users with the role "doctor".

      :param token: JWT token for authorization.
      :param db: Database session.
      :raises HTTPException:
      If the credentials are invalid or the role is not "doctor".
      :return: A list of patients.
      """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        role = payload.get("role")
        if username is None or role != "doctor":
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    patients = db.query(Patient).all()
    return patients
