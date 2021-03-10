# Use Python 3.8 buster for uwsgi
FROM python:3.8-buster

ENV MONGO_USERNAME = "root"
ENV MONGO_PASSWORD = "admin"
ENV FLASK_ENV="production"
ENV DB_NAME = "filed-audio-api-db"

# Working Directory
WORKDIR /api

ADD . /api

RUN pip install -r requirements.txt




CMD ["uwsgi", "api.ini"]