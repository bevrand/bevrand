const express = require('express');
const path = require('path');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const rp = require('request-promise');
const debug = require('debug')('bevrand.frontend:app');

const config = require('./config');

var app = express();

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
//TODO: check if this might not be needed anymore
app.use(express.static(path.join(__dirname, 'public')));


/**
 * API routes
 */
app.get('/api/frontpagelists', (req, res, next) => {
  rp(`${config.mongoApi}/api/frontpage`)
    .then(result => {
      debug('Got successful result from /frontpagelists: ' + result);
      return res.send(result);
    })
    .catch(err => {
      debug('Got error from frontpagelists' + err);
      return next(err);
    });
});

app.get('/api/frontpagelist', (req, res, next) => {
  if(!req.query.list){
    let err = new Error('Required parameter list was not specified');
    debug('Error: required parameter list not specified');
    err.status = 400;
    return next(err);
  }

  rp(`${config.mongoApi}/api/frontpage?list=${req.query.list}`)
    .then(result => {
      debug('Got successful result from /frontpageList: ' + result);
      return res.send(result);
    })
    .catch(err => {
      debug('Got error from frontpageLists' + err);
      return next(err);
    });
});

app.get('/api/randomize', (req, res, next) => {
  if(!req.query.user || !req.query.list){
    let err = new Error('Required parameters are user and list');
    err.status = 400;
    return next(err);
  }

  rp(`${config.randomizerApi}/api/randomize?user=${req.query.user}&list=${req.query.list}`)
    .then(result => {
      debug('Got successful result from /randomize: ' + result);
      return res.send(result);
    })
    .catch(err => {
      debug('Got error from frontpageLists' + err);
      return next(err);
    });
});

app.get('/api/redisuser', (req, res, next) => {
  if(!req.query.user || !req.query.list){
    let err = new Error('Required parameters are user and list');
    err.status = 400;
    return next(err);
  }

  rp(`${config.randomizerApi}/api/redisuser?user=${req.query.user}&list=${req.query.list}`)
    .then(result => {
      debug('Got successful result from /redisuser: ' + result);
      return res.send(result);
    })
    .catch(err => {
      debug('Got error from redisuser request' + err);
      return next(err);
    });
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.send(err);
});

module.exports = app;
