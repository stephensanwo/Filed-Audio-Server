# Use Python 3.8 buster for uwsgi
FROM python:3.8-buster


# Working Directory
WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["uwsgi", "api.ini"]