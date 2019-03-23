const express = require('express');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const swaggerUi = require('swagger-ui-express');
const yamljs = require('yamljs');
const config = require('../config');
const routes = require('./routes');
const { errorHandler, setHttpStatus, notFoundHandler } = require('./middlewares/errorHandling');

const swaggerDocument = yamljs.load('swagger.yaml');

const app = express();

app.use((req, res, next) => {
  //Only needed when running react app locally
  if (config.env === 'development' || config.env === 'local') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-type,Authorization');
  }
  next();
});

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());

app.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// TODO: CORS needed for routes, in case of local testing?

/**
 * API routes
 */
app.use('/', routes);

// catch 404 and forward to error handler
app.use(notFoundHandler);

app.use(setHttpStatus);

app.use(errorHandler);


module.exports = app;
