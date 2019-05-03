FROM cypress/base:10
WORKDIR /app

# This layer is cached
COPY package.json .

# by setting CI environment variable we switch the Cypress install messages
# to small "started / finished" and avoid 1000s of lines of progress messages
ENV CI=1
RUN npm install
# verify that Cypress has been installed correctly.
# running this command separately from "cypress run" will also cache its result
# to avoid verifying again when running the tests
RUN npx cypress verify

COPY cypress cypress
COPY cypress.json .