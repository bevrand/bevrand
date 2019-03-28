const { validateSignedPayloadImproved } = require('../services/jwtTokens');

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
  // TODO: do validation
  next();
};
