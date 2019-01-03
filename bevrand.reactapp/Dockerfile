# -- REACTJS BUILD environment --
FROM node:8.11-alpine as builder

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy package.json first, so dependencies can be installed seperately
COPY package.json /usr/src/app/package.json
RUN npm install --silent
RUN npm rebuild node-sass-chokidar

COPY . /usr/src/app
RUN npm run build

# -- NGINX - environment --
FROM nginx:stable-alpine

# Default config of Nginx needs change for React Router
RUN rm -rf /etc/nginx/conf.d
COPY conf /etc/nginx

COPY --from=builder /usr/src/app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]