const express = require('express');
const path = require('path');
const request = require('request');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const exjwt = require('express-jwt');
const rp = require ('request-promise');
const Promise = require('bluebird');
const jwt = require("jsonwebtoken");
const cors = require('cors');
const config = require('./config');
const swaggerUi = require('swagger-ui-express');
const yamljs = require('yamljs');
const swaggerDocument = yamljs.load('./swagger.yaml');

const controllers = require('./controllers');

const app = express();

app.use((req, res, next) => {
  //Only needed when running react app locally
  if(config.env === 'development'){
    res.setHeader('Access-Control-Allow-Origin', '*');
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

app.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

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
 * CORS Pre-Flight enabled routes
 */
app.options('/api/randomize', cors());
app.options('/api/register', cors());
app.options('/api/login', cors());
app.options('/api/user', cors());
app.options('/api/v2/frontpage', cors());
app.options('/api/v2/randomize', cors());

/**
 * API routes
 */
app.get('/api/frontpage', requestPipe(config.playlistApi));

const frontpageWithSignature = (url) => {
  return (req, res, next) => {

    
    rp({
      method: 'GET',
      uri: `${url}/api/frontpage`
    }).then(result => {
      

      let newResult = JSON.parse(result).map(item => {
        let signedItem = jwt.sign(item, config.frontendJwtSecret, { mutatePayload: true});
        item.jwtheader = JSON.parse(Buffer.from(signedItem.split('.')[0], 'base64').toString("ascii"));
        item.jwttoken = signedItem.split('.')[2];
        return item;
      });

      return res.send(newResult);
    }).catch(err => {
      console.error(`Error: ${err.message}`);
      return next(err);
    });
  }  
}

/**
 * Gives the complete response from the playlist api at the endpoint /api/frontpage, 
 * signed with a JWT Token, IssuedAtTime property (iat) and a JWT Header, which describes the algorithm used.
 */
app.get('/api/v2/frontpage', frontpageWithSignature(config.playlistApi));

app.get('/api/playlists', (req, res, next) => {
  //TODO: add middleware that checks is user is authorized for the specified username
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

const validateJwtTokenFrontend = (req, res, next) => {
    try {
      let requestJwtHeader = req.body.jwtheader;
      let requestJwtToken = req.body.jwttoken;

      delete req.body.jwtheader;
      delete req.body.jwttoken;

      let signedItem = jwt.sign(req.body, config.frontendJwtSecret);
      let jwtheader = signedItem.split('.')[0];
      let jwttoken = signedItem.split('.')[2];

      if(requestJwtToken === jwttoken){
        return next();
      }

      const error = new Error('JWT Token does not validate');
      error.name = 'InvalidJwtToken';
      throw error;
    } catch(err) {
      return next(err);
    }
}

/**
 * 
 * @param {string} user 
 * @param {string} list 
 * @param {string[]} beverages 
 */
var RandomizeRequest = function (user, list, beverages) {
  this.user = user;
  this.list = list;
  this.beverages = beverages;
};

/**
 * Calls the backend randomize api with POST at endpoint /api/randomize
 * Takes from the post body (req.body) the properties user, list, and beverages.
 * @param {string} endpoint 
 */
const requestRandomizePost = (endpoint) => {
  return (req, res) => {
    request({
      method: 'POST',
      qs: req.query, 
      uri: endpoint + '/api/randomize',
      body: new RandomizeRequest(req.body.user, req.body.list, req.body.beverages),
      json: true
    }).pipe(res);
  }
}

app.post('/api/v2/randomize', validateJwtTokenFrontend, requestRandomizePost(config.randomizerApi));
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
