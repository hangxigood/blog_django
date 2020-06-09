#!/bin/sh

python3 manage.py collectstatic --noinput #没有被执行，容器中的static 文件夹是空的
python3 manage.py migrate
gunicorn blog.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/blog_project