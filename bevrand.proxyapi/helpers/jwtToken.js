const jwt = require('jsonwebtoken');
const config = require('../config');

const validateJwtTokenMiddleware = (req, res, next) => {
  try {
    let requestJwtHeader = req.body.jwtheader;
    
    let requestJwtToken = req.body.jwttoken;
    
    delete req.body.jwttoken;
    
    let requestJwtIssuedAtTime = req.body.iat;
    
    let requestPayload = req.body;
    
    let headerString = JSON.stringify(requestJwtHeader);

    if(headerString == undefined){
      headerString = requestJwtHeader;
    }

    if(headerString == undefined || requestJwtIssuedAtTime == undefined || requestJwtToken == undefined)
    {
      const error = new Error('JWT Token does not exits');
      error.name = 'InvalidJwtToken';
      throw error;
    }

    delete req.body.jwtheader;

    let buffer1 = new Buffer(headerString);
    let base64requestJwtHeader = buffer1.toString('base64');

    let payloadString = JSON.stringify(requestPayload, Object.keys(requestPayload).sort());
    console.log(payloadString);
    let buffer2 = new Buffer(payloadString);
    let base64requestPayload = buffer2.toString('base64');

    let jwtString = base64requestJwtHeader.replace(new RegExp("=", 'g'), "") + "." + base64requestPayload.replace(new RegExp("=", 'g'), "") + "." + requestJwtToken;

    console.log("Going to verify string: [" + jwtString + "]");
    
    // New, unordered, method
    try {
      jwt.verify(jwtString, config.frontendJwtSecret);
      return next();
    }
    catch(err) {
      console.log("Could not validate the JWT with ordered method.");
    }

    const error = new Error('JWT Token does not validate');
    error.name = 'InvalidJwtToken';
    throw error;
  } catch (err) {
    return next(err);
  }
};

const signObjectWithJwtToken = object => {
  //Add issued at time:
  object.iat = Math.floor(new Date().getTime()/1000);

  // This sorts the object when serializing it, allowing other libarries (such as GSON) 
  // to call the API with the properties in "wrong" order.
  stringifiedObject = JSON.stringify(object, Object.keys(object).sort());

  let signedItem = jwt.sign(stringifiedObject, config.frontendJwtSecret, { mutatePayload: false });
  //object.iat = JSON.parse(Buffer.from(signedItem.split('.')[1], 'base64').toString("ascii")).iat;
  object.jwtheader = JSON.parse(Buffer.from(signedItem.split('.')[0], 'base64').toString("ascii"));
  object.jwttoken = signedItem.split('.')[2];

  return object;
}

module.exports = { validateJwtTokenMiddleware, signObjectWithJwtToken }