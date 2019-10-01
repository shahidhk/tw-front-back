FROM node:latest as build-stage
WORKDIR /app
RUN git clone https://7884e5f1f3d276fbc68a41dffb2d6149bde849e6@github.com/abrasher/tw-webapp.git
RUN git pull
WORKDIR /app/tw-webapp
RUN npm install
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/tw-webapp/dist /app
COPY nginx.conf /etc/nginx/nginx.conf