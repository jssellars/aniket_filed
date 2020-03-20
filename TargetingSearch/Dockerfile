FROM python:3.7-alpine

RUN apk --update add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq

RUN mkdir /www
WORKDIR /www
COPY requirements.txt /www/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . /www/