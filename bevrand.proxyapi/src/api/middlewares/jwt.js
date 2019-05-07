const { validateSignedPayloadImproved, validateJwtHeader } = require('../services/jwtTokens');

exports.validateJwtInBody = (req, res, next) => {
  try {
    validateSignedPayloadImproved(req.body);

    // Remove jwttoken before sending it to randomize api
    delete req.body.jwtheader;
    delete req.body.jwttoken;
    next();
  } catch (err) {
    next(err);
  }
};

exports.validateJwtHeader = (req, res, next) => {
  if (!req.header('x-api-token')) {
    const err = new Error('No authentication token present');
    err.status = 401;

    next(err);
  }

  try {
    res.locals.user = validateJwtHeader(req.header('x-api-token'));
    next();
  } catch (decodingError) {
    let err = new Error('Invalid authentication token present');
    err.status = 401;

    next(err);
  }
};
