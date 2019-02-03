const jwt = require('jsonwebtoken');
const config = require('../../config/variables');

// Old method: validateJwtTokenMiddleware function (req, res, next) { requestJwtToken = req.body.jwttoken, delete req.body.jwtheader, req.body.jwttoken }

function validateSignedPayload(signedPayload) {
  const tokenToValidate = signedPayload.jwttoken;
  let signedItem = jwt.sign(signedPayload, config.frontendJwtSecret);
  let jwttoken = signedItem.split('.')[2];

  if (tokenToValidate !== jwttoken) {
    const error = new Error('JWT Token does not validate');
    error.status = 403;
    error.name = 'InvalidJwtToken';
    throw error;
  }

  return true;
}

const signObject = object => {
  let signedItem = jwt.sign(object, config.frontendJwtSecret, {
    mutatePayload: true,
  });
  object.jwtheader = JSON.parse(Buffer.from(signedItem.split('.')[0], 'base64').toString('ascii'));
  object.jwttoken = signedItem.split('.')[2];
  return object;
};

module.exports = { validateSignedPayload, signObject };
