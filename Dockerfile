FROM python:3.11-slim

WORKDIR /app

ADD src /app/
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
