#!/bin/sh

cd /app/tw-webapp
touch .env.local
printf "VUE_APP_API=eDfGfj041tHBYkX9" > .env.local
git pull
npm install
npm run build