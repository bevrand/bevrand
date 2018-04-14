const rp = require('request-promise');
const jwt = require('jsonwebtoken');
const debug = require('debug')('controllers:authentication');

const handleLogin = (url, secret, expirationTime) => {
  return (req, res, next) => {
    const { username, passWord } = req.body;
    
    //TODO: If email address is provided, we first need to retrieve the username and id
  
    if(!username || !passWord) {
      let err = new Error('Required body elements are not present');
      err.status = 400;
      return next(err);
    }
    //TODO: Add password hashing on client side, that needs to be decrypted here
    rp({
      method: 'POST',
      uri: `${url}/api/Validate`,
      body: req.body,
      json: true
    })
    .then((result) => {
      if(!result){
        return res.status(401).send({
          success: false,
          token: null,
          message: 'Username or password is incorrect'
        });
      } else {
        return rp({
          method: 'GET',
          uri: `${url}/api/Users?username=${username}`
        });
      }
    }).then((result) => {
      const { emailAddress, active, id } = JSON.parse(result);
      if(!active) {
        return res.status(403).send({
          success: false,
          token: null,
          message: 'User is not active'
        });
      }
      // Is authenitcationExpirationTime a number?
      let token = jwt.sign({ id:id, username: username }, secret, {expiresIn: expirationTime})
      return res.send({
        success: true,
        message: 'Succesfully authenticated User',
        token: token
      })
    })
    .catch((err) => {
      return next(err);
    });
  }
}

const registerUser = (authenticationUrl) => {
  return (req, res, next) => {  
    if(!req.body.username || !req.body.passWord || !req.body.emailAddress) {
      let err = new Error('Required body elements are not present');
      err.status = 400;
      return next(err);
    }
    rp({
      method: 'POST',
      uri: `${authenticationUrl}/api/Users`,
      body: {
        username: req.body.username,
        emailAddress: req.body.emailAddress,
        passWord: req.body.passWord,
        active: true
      },
      json: true
    }).then(result => {
      return res.send(result);
    }).catch(err => {
      debug(`Error: ${err.message}`);
      return next(err);
    });
  }  
}

module.exports = {
  handleLogin: handleLogin,
  registerUser: registerUser
};