const express = require('express');
const path = require('path');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const rp = require('request-promise');
const debug = require('debug')('bevrand.frontend:api');

const config = require('./config');

const controllers = require('./controllers');

const app = express();

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

/**
 * API routes
 */
app.get('/api/frontpagelists', 
  controllers.playlists.getFrontpageLists(config.mongoApi, config.randomizerApi)
);
//TODO: add route to retrieve playlists of other users

app.post('/api/redis', [(req, res, next) => {
  //TODO: refactor query checks into seperate module
  if (!req.query.list || !req.query.user) {
    let err = new Error('Required parameter list or user was not specified');
    debug('Error: required parameter list not specified');
    err.status = 400;
    return next(err);
  } else {
    return next();
  }
}, controllers.redis.getRedis(config.randomizerApi)
]);

app.post('/api/randomize', [(req, res, next) => {
  if (!req.query.user || !req.query.list) {
    let err = new Error('Required query parameters are not present');
    err.status = 400;
    return next(err);
  } else if(!Array.isArray(req.body.beverages)){
    let err = new Error('The POST body does not contain a beverages array');
    err.status = 400;
    return next(err);
  } else {
    return next();
  }
}, controllers.randomize.getRandomize(config.randomizerApi)
]);

// catch 404 and forward to error handler
app.use((req, res, next) => {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use((err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') !== 'production' ? err : {};

  // render the error page
  let responseStatus = err.status || 500;
  console.error(err);
  res.status(responseStatus).send({
    result: 'error',
    message: err.message,
    httpstatus: responseStatus
  });
});

module.exports = app;
