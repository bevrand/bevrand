const rp = require('request-promise');
const debug = require('debug')('controllers:randomize');

const getRandomize = (randomizeApiUrl) => {
  return (req, res, next) => {    
    rp({
      method: 'POST',
      uri: `${randomizeApiUrl}/api/randomize`,
      body: {
        user: req.body.user,
        list: req.body.list,
        beverages: req.body.beverages
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

module.exports = {
  getRandomize: getRandomize
};