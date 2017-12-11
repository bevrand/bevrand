FROM node:8.9-alpine

#copy directory
COPY . /frontend
COPY package.json /frontend/package.json

#TODO: add a way to install both client and api modules
#TODO: Build the client
#TODO: Bundle build client to the public folder of the nodejs api

# set working directory
WORKDIR /frontend

# install modules
RUN npm install --quiet


# port to expose
EXPOSE 4540

#TODO: make production running of app by using pm2

# run app
CMD ["npm","start"]
