# -- NGINX - environment --
FROM nginx:stable-alpine

# Copy files and directories from the application
COPY ./nginx.conf.d/ /etc/nginx/conf.d/

# Open port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
