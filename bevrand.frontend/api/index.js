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

/**
 * Uses the provided Playlist to randomize a beverage
 * @param {object} playlist
 */
const randomizeBeverageMock = (playlist) => {
  const amountOfBeverages = playlist.length;
  const randomizedIndex = Math.floor(Math.random() * (amountOfBeverages));
  return playlist[randomizedIndex];
};

/**
 * API routes
 */
app.get('/api/frontpagelists', (req, res, next) => {
  //Optional usage of mock if config specifies it
  if(config.useMock){
    const mockData = require('./mockdata');
    return res.send({playlists: mockData});
  }

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
      })
    })
    .catch(err => {
      debug('Got error from frontpagelists' + err);
      return next(err);
    });
});

app.get('/api/frontpagelist', (req, res, next) => {
  if(!req.query.list || !req.query.user){
    let err = new Error('Required parameter list or user was not specified');
    debug('Error: required parameter list not specified');
    err.status = 400;
    return next(err);
  }

  rp(`${config.mongoApi}/api/frontpage?list=${req.query.list}&user=${req.query.user}`)
    .then(result => {
      debug('Got successful result from /frontpageList: ' + result);
      return res.send(result);
    })
    .catch(err => {
      debug('Got error from frontpageLists' + err);
      return next(err);
    });
});

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

  if(config.useMock){
    let beverage = randomizeBeverageMock(beverages);
    debug('Used Mock to randomize the beverage');
    return res.send(beverage);
  }
  debug('Using api to randomize beverage');

  let options = {
    method: 'POST',
    uri: `${config.randomizerApi}/api/randomize?user=${user}&list=${list}`,
    body: {
      user: user,
      list: list,
      beverages: beverages
    },
    json: true
  };

  //TODO: add redis api results to the result
  rp(options)
    .then(result => res.send({ result: result}))
    .catch(err => {
      // console.log(err);
      debug(`Error: ${err.message}`);
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
