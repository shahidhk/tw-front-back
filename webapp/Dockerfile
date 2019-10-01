FROM node:latest as build-stage
WORKDIR /app
RUN git clone https://7884e5f1f3d276fbc68a41dffb2d6149bde849e6@github.com/abrasher/tw-webapp.git
WORKDIR /app/tw-webapp
RUN git pull
RUN npm install
RUN npm run build