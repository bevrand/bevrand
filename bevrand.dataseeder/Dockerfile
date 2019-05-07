FROM python:3.7.3-slim
#-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
ADD . /usr/src/app

#ENV PYTHONPATH /absolute/path/to/the/pythonpath/inside/the/container
ENV PYTHONPATH ./

# run server
CMD python -u ./seeder.py