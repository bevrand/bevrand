const jwt = require('jsonwebtoken');
const config = require('../../config');

// Old method: validateJwtTokenMiddleware function (req, res, next) { requestJwtToken = req.body.jwttoken, delete req.body.jwtheader, req.body.jwttoken }

function validateJwtHeader(jwtHeader) {
  return jwt.verify(jwtHeader, config.authenticationSecret);
}

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

function validateSignedPayloadImproved(signedPayload) {
  let requestJwtHeader = signedPayload.jwtheader;
  let requestJwtToken = signedPayload.jwttoken;
  delete signedPayload.jwttoken;
  delete signedPayload.jwtheader;
  let requestJwtIssuedAtTime = signedPayload.iat;
  let requestPayload = signedPayload;
  let headerString = JSON.stringify(requestJwtHeader);

  if (!headerString) {
    headerString = requestJwtHeader;
  }

  if (!headerString || !requestJwtIssuedAtTime || !requestJwtToken) {
    const error = new Error('JWT Token does not exits');
    error.name = 'InvalidJwtToken';
    throw error;
  }

  let buffer1 = new Buffer(headerString);
  let base64requestJwtHeader = buffer1.toString('base64');

  let payloadString = JSON.stringify(requestPayload, Object.keys(requestPayload).sort());

  let buffer2 = new Buffer(payloadString);
  let base64requestPayload = buffer2.toString('base64');

  let jwtString = base64requestJwtHeader
      .replace(new RegExp("=", 'g'), "") + "." + base64requestPayload
      .replace(new RegExp("=", 'g'), "") + "." + requestJwtToken;

  try {
    return jwt.verify(jwtString, config.frontendJwtSecret);
  }
  catch(err) {
    const error = new Error('JWT Token does not validate');
    error.name = 'InvalidJwtToken';
    throw error;
  }
}

function signObject(object) {
  //Add issued at time:
  object.iat = Math.floor(new Date().getTime() / 1000);

  // This sorts the object when serializing it, allowing other libraries (such as GSON)
  // to call the API with the properties in "wrong" order.
  let stringifiedObject = JSON.stringify(object, Object.keys(object).sort());

  let signedItem = jwt.sign(stringifiedObject, config.frontendJwtSecret, { mutatePayload: false });
  //object.iat = JSON.parse(Buffer.from(signedItem.split('.')[1], 'base64').toString("ascii")).iat;
  object.jwtheader = JSON.parse(Buffer.from(signedItem.split('.')[0], 'base64').toString('ascii'));
  object.jwttoken = signedItem.split('.')[2];
  return object;
}

module.exports = {
  validateSignedPayload,
  validateSignedPayloadImproved,
  validateJwtHeader,
  signObject,
};
