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
app.use(express.static(path.join(__dirname, 'public')));


/**
 * Uses the provided Playlist to randomize a beverage
 * @param {object} playlist
 */
const randomizeBeverageMock = (playlist) => {
  const amountOfBeverages = playlist.beverages.length;
  const randomizedIndex = Math.floor(Math.random() * (amountOfBeverages));
  return playlist.beverages[randomizedIndex];
};

/**
 * API routes
 */
app.get('/api/frontpagelists', (req, res, next) => {
  const playlistData = [
    {
      id: 0,
      name: "Girls night out",
      fullImageUrl: "img/portfolio/fullsize/Girls night out - small.jpg",
      thumbImageUrl: "img/portfolio/thumbnails/Girls night out - small.jpg",
      beverages: [
        "melk",
        "bier",
        "wijn",
        "fruitsapje",
        "test succesful"
      ]
    },
    {
      id: 1,
      name: "Highland Games",
      fullImageUrl: "img/portfolio/fullsize/Highland Games - small.jpg",
      thumbImageUrl: "img/portfolio/thumbnails/Highland Games - small.jpg",
      beverages: [
        "Palm",
        "Tripel",
        "wijn",
        "fruitsapje"
      ]
    },
    {
      id: 2,
      name: "Mancave mayhem",
      fullImageUrl: "img/portfolio/fullsize/Mancave mayhem - small.jpg",
      thumbImageUrl: "img/portfolio/thumbnails/Mancave mayhem - small.jpg",
      beverages: [
        "Champagne",
        "Rode wijn",
        "Witte wijn"
      ]
    },
    {
      id: 3,
      name: "Office madness",
      fullImageUrl: "img/portfolio/fullsize/Office madness - small.jpg",
      thumbImageUrl: "img/portfolio/thumbnails/Office madness - small.jpg",
      beverages: [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
      ]
    },
    {
      id: 4,
      name: "TGIF",
      fullImageUrl: "img/portfolio/fullsize/Thank god it's friday - small.jpg",
      thumbImageUrl: "img/portfolio/thumbnails/Thank god it's friday - small.jpg",
      beverages: [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
      ]
    },
    {
      id: 5,
      name: "Happy Holidays",
      fullImageUrl: "img/portfolio/fullsize/The most wonderful time - small.jpg",
      thumbImageUrl: "img/portfolio/thumbnails/The most wonderful time - small.jpg",
      beverages: [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
      ]
    }
  ];
  // rp(`${config.mongoApi}/api/frontpage`)
  //   .then(result => {
  //     debug('Got successful result from /frontpagelists: ' + result);
  //     return res.send(result);
  //   })
  //   .catch(err => {
  //     debug('Got error from frontpagelists' + err);
  //     return next(err);
  //   });
  res.send({ playlists: playlistData });
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

app.post('api/randomize', (req, res, next) => {
  if(!req.query.user || !req.query.list){
    let err = new Error('Required Parameters are user and list');
    err.status = 400;
    return next(err);
  }

  let playlist = req.body.playlist;
  let list = req.query.list;
  let user = req.query.user;
  debug(`api/randomize: Received parameters, playlist: ${playlist}, list: ${list}, user:${user}`);

  if(config.env !== 'production'){
    let beverage = randomizeBeverageMock(playlist);
    debug('Used Mock to randomize the beverage');
    return res.send({ result: beverage});
  }
  debug('Using api to randomize beverage');

  let options = {
    method: 'POST',
    uri: `${config.randomizerApi}/api/randomize?user=${user}&list=${list}`,
    body: {
      user: user,
      list: list,
      beverages: playlist
    },
    json: true
  };

  rp(options)
    .then(result => res.send({ result: result}))
    .catch(err => {
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
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.send(err);
});

module.exports = app;
