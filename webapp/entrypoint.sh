#!/bin/sh

cd /app/tw-webapp
touch /app/tw-webapp/.env.local
printf "VUE_APP_API=eDfGfj041tHBYkX9\n" >> /app/tw-webapp/.env.local
printf "VUE_APP_URL=$VUE_APP_URL\n" >> /app/tw-webapp/.env.local
git fetch --all
git reset --hard origin/master
npm install
npm run build