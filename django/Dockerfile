# pull official base image
FROM python:3.8-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/django

# install psycopg2
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/django/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/django/

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/django/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/django/entrypoint.sh"]
