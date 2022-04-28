# Frontend
FROM python:3.7-alpine

ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG POSTGRES_HOST

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/api

COPY . .
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_HOST=${POSTGRES_HOST}

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install -r requirements.txt --default-timeout=100 future \
    && apk del .build-deps

ENV FLASK_APP=flaskr

RUN chmod 755 entrypoint.sh
ENTRYPOINT ["/usr/src/app/api/entrypoint.sh"]

EXPOSE 5000