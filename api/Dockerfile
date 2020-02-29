FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install fastapi[all] gunicorn motor
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
