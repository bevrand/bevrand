FROM node:8.11-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy package.json first, so dependencies can be installed seperately
COPY package.json /usr/src/app/package.json
RUN npm install --silent

COPY . /usr/src/app

EXPOSE 5000
CMD ["node", "server.js"]