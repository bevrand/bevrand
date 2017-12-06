FROM node:8.9-alpine

#copy directory
COPY . /nodefrontend
COPY package.json /nodefrontend/package.json

# set working directory
WORKDIR /nodefrontend

# install modules
RUN npm install --quiet

# port to expose
EXPOSE 4540

# run app
CMD ["npm","start"]
