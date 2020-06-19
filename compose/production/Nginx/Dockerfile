FROM nginx:1.19-alpine

# 设置时区为上海
RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

# 删除原有.conf 文件，复制自己的配置文件
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/Nginx/blog.conf /etc/nginx/conf.d/blog.conf