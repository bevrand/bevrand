const rp = require('request-promise');
const jwt = require('jsonwebtoken');
const debug = require('debug')('controllers:authentication');

const handleLogin = (url, secret, expirationTime) => {
  return (req, res, next) => {
    const { userName, passWord, emailAddress } = req.body;
  
    if(!(userName || emailAddress) || !passWord) {
      let err = new Error('Required body elements are not present');
      err.status = 400;
      return next(err);
    }
    
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
          uri: `${url}/api/Users/by-username/${userName}`
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
      let token = jwt.sign({ id:id, username: userName }, secret, {expiresIn: expirationTime})
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
    const { userName, passWord, emailAddress } = req.body;
    
    if(!userName || !passWord || !emailAddress) {
      let err = new Error('Required body elements are not present');
      err.status = 400;
      return next(err);
    }

    rp({
      method: 'POST',
      uri: `${authenticationUrl}/api/Users`,
      body: req.body,
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