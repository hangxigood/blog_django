FROM python:3.8

ENV PYTHONUNBUFFERED 1

# 设置时区为上海
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR /blog_project

COPY requirements.txt /blog_project/

RUN pip install -r /blog_project/requirements.txt

COPY . /blog_project

COPY ./compose/production/Django/start.sh /start.sh

RUN chmod +x /start.sh