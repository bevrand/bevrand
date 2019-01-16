const express = require('express');
const path = require('path');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const cors = require('cors');
const config = require('./config');
const routes = require('./routes');

const app = express();

app.use((req, res, next) => {
  //Only needed when running react app locally
  if(config.env === 'development' || config.env === 'local'){
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-type,Authorization');
  }
  next();
});

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

/**
 * CORS Pre-Flight enabled routes
 */
app.options('/api/register', cors());
app.options('/api/login', cors());
app.options('/api/user', cors());
app.options('/api/v2/frontpage', cors());
app.options('/api/v2/randomize', cors());

/**
 * API routes
 */
app.use('/api', routes.authentication);
app.use('/api', routes.playlist);
app.use('/api', routes.randomizer);
app.use('/api', routes.swagger);

// catch 404 and forward to error handler
app.use((req, res, next) => {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler of authentication module
app.use((err, req, res, next) => {
  if(err.name === 'InvalidJwtToken') {
    err.status = 400;
  }
  else if(err.name === 'UnauthorizedError') {
    err.status = 401;
  } 
  next(err);  
});

// error handler
app.use((err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') !== 'production' ? err : {};
  
  // Only log when not in production env
  if(req.app.get('env') !== 'production') {
    console.error(err);
  }
  

  // render the error page
  let responseStatus = err.status || err.statusCode || 500;
  res.status(responseStatus).send({
    result: 'error',
    message: err.message,
    httpstatus: responseStatus
  });
});

module.exports = app;
