FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                postgresql-dev \
        ;

# 设置时区为上海
RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

RUN mkdir /blog_project

WORKDIR /blog_project

COPY requirements.txt /blog_project/

RUN pip install -r /blog_project/requirements.txt -i https://pypi.douban.com/simple

COPY ./compose/local/Django/start.sh /start.sh

RUN chmod +x /start.sh