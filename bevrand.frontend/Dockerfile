FROM node:8.9-slim

#copy directory
COPY . /frontend
# COPY package.json /frontend/package.json


#TODO: add a way to install both client and api modules
#TODO: Build the client on production way
#TODO: Bundle build client to the public folder of the nodejs api

# set working directory
WORKDIR /frontend/client

# install modules
RUN npm install --quiet

RUN npm rebuild node-sass-chokidar

RUN npm install -g serve

RUN npm run build


# port to expose
EXPOSE 5000

# run app
CMD ["serve","-s", "build"]
