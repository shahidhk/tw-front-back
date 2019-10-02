FROM node:latest
WORKDIR /apollo
COPY helpers.js /apollo/helpers.js
COPY index.js /apollo/index.js
COPY package.json /apollo/package.json
RUN npm install
RUN npm start