FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

WORKDIR /app

ADD src /app/
RUN pip3 install -r requirements.txt

CMD exec gunicorn --bind :5000 --workers 1 --threads 1 --timeout 0 app:app
