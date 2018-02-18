const rp = require('request-promise');
const debug = require('debug')('controllers:randomize');
const { addHistoryToBeverage } = require('../helpers/data');

const getRandomize = (randomizeApiUrl) => {
  return (req, res, next) => {
    const beverages = req.body.beverages.map(elem => {
      return elem.drink;
    });
    const list = req.query.list;
    const user = req.query.user;
    debug(`api/randomize: Received parameters, playlist: ${beverages}, list: ${list}, user:${user}`);
    
    let randomizedBeverage;
    rp({
      method: 'POST',
      uri: `${randomizeApiUrl}/api/randomize?user=${user}&list=${list}`,
      body: {
        user: user,
        list: list,
        beverages: beverages
      },
      json: true
    }).then(result => {
      randomizedBeverage = result;
      return rp(`${randomizeApiUrl}/api/redis?user=${user}&list=${list}&topfive=false`);
    }).then(redisResult => {
      let parsedRedisResult = JSON.parse(redisResult);
      let newBeverages = addHistoryToBeverage(beverages, parsedRedisResult[`${user}:${list}`])
      return res.send({
        result: randomizedBeverage,
        history: newBeverages
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