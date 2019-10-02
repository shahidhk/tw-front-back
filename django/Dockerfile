# pull official base image
FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/django

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add linux-headers \
    && pip install psutil \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/django/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/django/

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/django/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/django/entrypoint.sh"]
