#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn blog.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/blog_project


