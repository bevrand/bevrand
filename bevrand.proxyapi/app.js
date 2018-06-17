const express = require('express');
const path = require('path');
const request = require('request');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const exjwt = require('express-jwt');
const rp = require ('request-promise');
const Promise = require('bluebird');

const config = require('./config');

const controllers = require('./controllers');

const app = express();

app.use((req, res, next) => {
  //Only needed when running react app locally
  if(config.env === 'development'){
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
    res.setHeader('Access-Control-Allow-Headers', 'Content-type,Authorization');
  }
  
  next();
});

const jwtMW = exjwt({
  secret: config.authenticationSecret
});

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

/**
 * Util to pipe requests to another endpoint
 * @param {string} endpoint 
 */
const requestPipe = (endpoint) => {
  return (req, res) => {
    const url = endpoint + req.url;
    req.pipe(request({ qs: req.query, uri: url })).pipe(res);
  }
}

/**
 * Util to pipe requests to another endpoint
 * Also pipes the post body
 * @param {string} endpoint 
 */
const requestPipePost = (endpoint) => {
  return (req, res) => {
    request({
      method: 'POST',
      qs: req.query, 
      uri: endpoint + req.url,
      body: req.body,
      json: true
    }).pipe(res);
  }
}

/**
 * API routes
 */
app.get('/api/frontpage', requestPipe(config.playlistApi));

app.get('/api/playlists', (req, res, next) => {
  const { username } = req.query;
  if(!username){
    let err = new Error('Required parameters are not present');
    err.status = 400;
    return next(err);
  }

  rp(`${config.playlistApi}/api/user?user=${username}`)
    .then(result => {
      let parsedResult = JSON.parse(result);
      return parsedResult.lists;
    })
    .then(result => {
      let promises = result.map(value => {
        return rp(`${config.playlistApi}/api/list?user=${username}&list=${value}`)
          .then(response => { 
            return JSON.parse(response); 
          });
      });

      Promise.all(promises).then(results => {
        console.log('Results of promise all: ', results);
        res.send(results);
      })
    })
    .catch(err => {
      return next(err);
    });
});

app.get('/api/user', requestPipe(config.playlistApi));

app.post('/api/user', requestPipePost(config.playlistApi));

app.get('/api/redis', requestPipe(config.randomizerApi));

app.post('/api/randomize', requestPipePost(config.randomizerApi));

app.post('/api/login', 
  controllers.authentication.handleLogin(
    config.authenticationApi, 
    config.authenticationSecret, 
    config.authenticationExpirationTime
  )
);

app.post('/api/register', 
  controllers.authentication.registerUser(config.authenticationApi)
);

app.get('/test/validateJWT', jwtMW, (req, res)=> {
  res.send('You are authenticated');
})

// catch 404 and forward to error handler
app.use((req, res, next) => {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler of authentication module
app.use((err, req, res, next) => {
  if(err.name === 'UnauthorizedError') {
    res.status(401).send(err);
  } else {
    next(err);
  }
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
