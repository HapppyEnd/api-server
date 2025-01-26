FROM python:3.12

WORKDIR /app

COPY ../code_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../ .

EXPOSE 8000

CMD ["uvicorn", "code_app.main_app:app", "--host", "0.0.0.0", "--port", "8000"]