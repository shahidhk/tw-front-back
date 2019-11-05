#!/bin/sh
echo "################################## Run nginx"
export DOLLAR='$'
envsubst < /app/nginx.conf.template > /config/env.nginx.conf
envsubst < /app/nginx.conf.template > /config/nginx/site-confs/default
