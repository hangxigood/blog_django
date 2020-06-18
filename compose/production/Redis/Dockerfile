FROM redis
COPY compose/production/Redis/redis.conf /usr/local/etc/redis/redis.conf

# 设置时区为上海
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]