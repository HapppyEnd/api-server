# API Server

## Description

This is a FastAPI-based web application that provides an API for managing users and patients. It includes user authentication with JWT tokens and role-based access control.

## Features

- User authentication with JWT tokens
- Role-based access control
- Secure password hashing
- Database migrations with Alembic

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/HapppyEnd/api-server
    cd api_server
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r code_app/requirements.txt
    ```

4. Set up the database:
    ```sh
    alembic upgrade head
    ```

## Environment Variables

You need to set the following environment variables for the application to run properly. You can create a `.env` file in the root directory of the project:

```sh
DATABASE_URL=postgresql://user:password@localhost/mydatabase
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Description of Variables:
`DATABASE_URL`: The URL for connecting to your database (PostgreSQL or SQLite).

`SECRET_KEY`: A secret key used for encoding the JWT tokens.

`ALGORITHM`: The algorithm used for JWT encoding (default is HS256).

`ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for access tokens in minutes.

## Usage
### Run the FastAPI server:

```sh
uvicorn code_app.main_app:app --reload
```
Access the API documentation at http://127.0.0.1:8000/docs.

### Run the tests located in the tests folder:
```sh
pytest tests
```
To run the tests with coverage, use:

```sh
pytest --cov=code_app tests
```
## API Endpoints
### Authentication
**POST** `/login`

- **Description**: Authenticates a user and returns a JWT token.
- **Request Body**:
    - `username`: The username of the user.
    - `password`: The user's password.
- **Responses**:
    - `200 OK`: Returns the access token and token type.
    - `401 Unauthorized`: Invalid credentials.
### Patients
**GET** `/patients`
- **Description**: Retrieves a list of patients. Accessible only to users with the role "doctor".
- **Headers**:
    - `Authorization`: Bearer token.
- **Responses**:
    - `200 OK`: Returns a list of patients.
    - `401 Unauthorized`: Not authenticated or role is not "doctor".

## Running with Docker Compose
To build and run the application with Docker Compose, use the following command:
```sh
docker-compose up --build
```
The application will be accessible at http://localhost:8000.