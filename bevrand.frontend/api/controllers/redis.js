const rp = require('request-promise');
const debug = require('debug')('controllers:redis');

const getRedis = (randomizeApiUrl) => {
  return (req, res, next) => {
    const list = req.query.list;
    const user = req.query.user;
    const topfive = req.query.topfive;

    rp(`${randomizeApiUrl}/api/redis?user=${user}&list=${list}&topfive=${topfive}`)
      .then(result => {
        const resultJson = JSON.parse(result);
        
        debug('Got succesful result from /redis: ', resultJson);
        return res.send(resultJson);
      })
      .catch(err => {
        debug('Got error from randomizer api, redis route: ' + err);
        return next(err);
      });
  }
}

module.exports = {
  getRedis: getRedis
};