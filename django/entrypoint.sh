#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
ls
cd /django
ls
# python manage.py flush --no-input
python SAIS_API/manage.py migrate
# python manage.py collectstatic --no-input
exec "$@"
