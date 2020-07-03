#!/bin/sh

python3 manage.py collectstatic --noinput
# python manage.py makemigrations
python3 manage.py migrate
gunicorn blog.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/blog_project