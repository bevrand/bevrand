const express = require('express');
const logger = require('morgan');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const swaggerUi = require('swagger-ui-express');
const yamljs = require('yamljs');
const routes = require('./routes');
const { errorHandler, setHttpStatus, notFoundHandler } = require('./middlewares/errorHandling');

const swaggerDocument = yamljs.load('swagger.yaml');

const app = express();

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');

  next();
});

app.options('*', cors());

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());

app.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

/**
 * API routes
 */
app.use('/', routes);

// catch 404 and forward to error handler
app.use(notFoundHandler);

app.use(setHttpStatus);

app.use(errorHandler);

module.exports = app;
