FROM linuxserver/letsencrypt
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./nginx.conf.template /app/nginx.conf.template
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
