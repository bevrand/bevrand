FROM node:8.9-slim

#copy directory
COPY . /frontend

# set working directory
WORKDIR /frontend/client

# install & build for the client directory
RUN npm install --quiet

RUN npm rebuild node-sass-chokidar

RUN npm run build

# Copy build results to public folder of api
RUN cp -rn build/* ../api/public

WORKDIR ../api

# Install dependencies for the api
RUN npm install --quiet

WORKDIR ../

RUN npm install --quiet

# port to expose
EXPOSE 5000

# Run the app
CMD ["npm","run", "server"]

