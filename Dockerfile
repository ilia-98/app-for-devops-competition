# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev libssl-dev libpq-dev gcc sqlite3 libsqlite3-dev
RUN mkdir /db
RUN /usr/bin/sqlite3 /db/messages.db
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3","./main.py"]
