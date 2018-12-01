const jwt = require('jsonwebtoken');
const config = require('../config');

const validateJwtTokenMiddleware = (req, res, next) => {
  try {
    // let requestJwtHeader = req.body.jwtheader;
    let requestJwtToken = req.body.jwttoken;

    delete req.body.jwtheader;
    delete req.body.jwttoken;

    let signedItem = jwt.sign(req.body, config.frontendJwtSecret);
    // let jwtheader = signedItem.split('.')[0];
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
};

module.exports = { validateJwtTokenMiddleware }