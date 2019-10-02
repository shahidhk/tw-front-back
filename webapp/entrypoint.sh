#!/bin/sh

cd /app/tw-webapp
git pull
npm install
npm run build