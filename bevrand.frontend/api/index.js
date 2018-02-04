const express = require('express');
const path = require('path');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const rp = require('request-promise');
const Promise = require('bluebird');
const debug = require('debug')('bevrand.frontend:api');

const config = require('./config');

var app = express();

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

//TODO: Refactor into seperate modules

/**
 * API routes
 */
app.get('/api/frontpagelists', (req, res, next) => {
  //TODO: Concat the results from the redis api for the default playlist
  rp(`${config.mongoApi}/api/frontpage`)
    .then(result => {
      debug('Got successful result from /frontpagelists: ' + result);
      let parsedResult = JSON.parse(result);
      return parsedResult.front_page_lists;
    })
    .then((result) => {
      let promises = result.map(value => {
        return rp(`${config.mongoApi}/api/frontpage?list=${value}`)
          .then(response => { 
            return JSON.parse(response); 
          });
      });

      Promise.all(promises).then(results => {
        debug('Sending results', results);
        res.send({playlists: results});
      });
    })
    .catch(err => {
      debug('Got error from frontpagelists' + err);
      return next(err);
    });
});

//TODO: add route to retrieve playlists of other users

app.get('/api/redis', (req, res, next) => {
  if(!req.query.list || !req.query.user){
    let err = new Error('Required parameter list or user was not specified');
    debug('Error: required parameter list not specified');
    err.status = 400;
    return next(err);
  }

  rp(`${config.randomizerApi}/api/redis?user=${req.query.user}&list=${req.query.list}&topfive=false`)
    .then(result => {
      debug('Got succesful result from /redis: ' + result);
      return res.send(result);
    })
    .catch(err => {
      debug('Got error from randomizer api, redis route' + err);
      return next(err);
    });
})

app.post('/api/randomize', (req, res, next) => {
  if(!req.query.user || !req.query.list){
    let err = new Error('Required query parameters are not present');
    err.status = 400;
    return next(err);
  }

  if(!Array.isArray(req.body.beverages)){
    let err = new Error('The POST body does not contain a beverages array');
    err.status = 400;
    return next(err);
  }

  const beverages = req.body.beverages;
  const list = req.query.list;
  const user = req.query.user;
  debug(`api/randomize: Received parameters, playlist: ${beverages}, list: ${list}, user:${user}`);
  
  let randomizedBeverage;
  rp({
    method: 'POST',
    uri: `${config.randomizerApi}/api/randomize?user=${user}&list=${list}`,
    body: {
      user: user,
      list: list,
      beverages: beverages
    },
    json: true
  }).then(result => {
    randomizedBeverage = result;
    return rp(`${config.randomizerApi}/api/redis?user=${user}&list=${list}&topfive=false`);
  }).then(result => {
    return res.send({ 
      result: randomizedBeverage,
      history: JSON.parse(result)
    });
  }).catch(err => {
    debug(`Error: ${err.message}`);
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
  res.locals.error = req.app.get('env') !== 'production' ? err : {};

  // render the error page
  let responseStatus = err.status || 500;
  res.status(responseStatus).send({
    result: 'error',
    message: err.message,
    httpstatus: responseStatus
  });
});

module.exports = app;
