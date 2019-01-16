FROM postgres:10.6-alpine

EXPOSE 5432
# run create.sql on init
ADD createdatabase.sql /docker-entrypoint-initdb.d
