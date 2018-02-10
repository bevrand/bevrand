const rp = require('request-promise');
const debug = require('debug')('controllers:redis');
const { mergeHistoryWithBeverage } = require('../helpers/data');

const getRedis = (randomizeApiUrl) => {
  return (req, res, next) => {
    const list = req.query.list;
    const user = req.query.user;
    const beverages = req.body.beverages;

    rp(`${randomizeApiUrl}/api/redis?user=${user}&list=${list}&topfive=false`)
      .then(result => {
        const resultJson = JSON.parse(result);
        const updatedBeveragesArray = mergeHistoryWithBeverage(beverages, resultJson[`${user}:${list}`])
        
        debug('Got succesful result from /redis: ', updatedBeveragesArray);
        return res.send(updatedBeveragesArray);
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