FROM node:lts-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy package.json first, so dependencies can be installed seperately
COPY package*.json /usr/src/app/
RUN npm ci --only=production

COPY . /usr/src/app

EXPOSE 5000
CMD ["node", "./src/server.js"]
