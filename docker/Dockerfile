FROM python:3.9-slim

WORKDIR /app

COPY ../code_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../code_app /app

EXPOSE 8000

CMD ["uvicorn", "main_app:app", "--host", "0.0.0.0", "--port", "8000"]