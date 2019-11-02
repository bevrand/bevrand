FROM python:3.7-alpine
# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

                          # Pillow dependencies on Alpine
RUN apk --no-cache add gcc \
                   python3-dev \
                   musl-dev \
                   jpeg-dev \
                   zlib-dev \
                   freetype-dev \
                   lcms2-dev \
                   openjpeg-dev \
                   tiff-dev \
                   tk-dev \
                   tcl-dev \
                   # tesseract dependencies
                   tesseract-ocr

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

EXPOSE 5000

# add app
ADD ./app.py /usr/src/app
ADD ./error_model.py /usr/src/app

# run server
#CMD python manage.py runserver -h 0.0.0.0
CMD gunicorn --bind 0.0.0.0:5000 app