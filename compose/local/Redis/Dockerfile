FROM redis
COPY compose/local/Redis/redis.conf /usr/local/etc/redis/redis.conf
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime # 确保时区与宿主机相同
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]