# -- NGINX - environment --
FROM nginx:stable-alpine

# Copy files and directories from the application
COPY index.html /usr/share/nginx/html
COPY images/ /usr/share/nginx/html/images/
COPY assets/ /usr/share/nginx/html/assets/

# Open port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]