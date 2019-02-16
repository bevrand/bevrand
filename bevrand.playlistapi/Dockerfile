FROM python:3.7.2-alpine3.8
CMD apk add curl
HEALTHCHECK --timeout=1s --interval=30s --retries=3 \
  CMD curl -s --fail http://playlistapi:5000/api/v1/public/ping || exit 1
# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Create a group and user
RUN addgroup --system --gid 4550 appgroup \
&& adduser --system -u 4550 --ingroup appgroup --shell /bin/sh appuser

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

EXPOSE 5000

# add app
ADD . /usr/src/app

# Make app directory content read-only, except for go executable
RUN chown -R 4550:4550 /usr/src/app && chmod -R u-x+X,go-rwx /usr/src/app

# Drop user
USER 4550:4550

# run server
#CMD python manage.py runserver -h 0.0.0.0
CMD gunicorn -w 1 -b 0.0.0.0:5000 manage:app
