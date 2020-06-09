FROM nginx:1.17.1

ADD https://dl.eff.org/certbot-auto /usr/local/bin/certbot-auto
RUN chown root /usr/local/bin/certbot-auto && \
    chmod 0755 /usr/local/bin/certbot-auto && \
    certbot-auto -n --install-only

RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/blog.conf /etc/nginx/conf.d/blog.conf
COPY ./compose/production/nginx/fullchain.pem /etc/letsencrypt/live/blog.frankxiang.xyz/