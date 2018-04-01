const rp = require('request-promise');
const debug = require('debug')('controllers:authentication');

const validateLogin = (authenticationUrl) => {
  return (req, res, next) => {    
    rp({
      method: 'POST',
      uri: `${authenticationUrl}/api/Validate`,
      body: {
        user: req.body.user,
        list: req.body.password
      },
      json: true
    }).then(result => {
      return res.send({
        result: result
      });
    }).catch(err => {
      debug(`Error: ${err.message}`);
      return next(err);
    });
  }
}

const registerUser = (authenticationUrl) => {
  return (req, res, next) => {    
    rp({
      method: 'POST',
      uri: `${authenticationUrl}/api/User`,
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
  validateLogin: validateLogin,
  registerUser: registerUser
};