const rp = require('request-promise');
const debug = require('debug')('controllers:playlists');
const Promise = require('bluebird');
const { addHistoryToBeverage } = require('../helpers/data');

const getFrontpageLists = (mongoApiurl, randomizerApiUrl) => {
  return (req, res, next) => {
    rp(`${mongoApiurl}/api/frontpage`)
      .then(result => {
        debug('Got successful result from /frontpagelists: ' + result);
        let parsedResult = JSON.parse(result);

        return parsedResult.front_page_lists;
      })
      .then((result) => {
        let promises = result.map(value => {
          let mongoResult;
          let mongoResultUser;
          return rp(`${mongoApiurl}/api/frontpage?list=${value}`)
            .then(response => {
              mongoResult = JSON.parse(response);
              mongoResultUser = mongoResult.user.toLowerCase();
              return rp(`${randomizerApiUrl}/api/redis?user=${mongoResultUser}&list=${mongoResult.name}&topfive=false`)
            })
            .then(result => {
              let redisHistory = JSON.parse(result);
              mongoResult.beverages = addHistoryToBeverage(mongoResult.beverages, redisHistory[`${mongoResultUser}:${mongoResult.name}`]);
              return mongoResult;
            })
            .catch(err => {
              return next(err);
            })
        });

        return Promise.all(promises);
      })
      .then(results => {
        debug('Sending results', results);
        return res.send({ playlists: results });
      })
      .catch(err => {
        debug('Got error from frontpagelists' + err);
        return next(err);
      });
  }
}

module.exports = {
  getFrontpageLists: getFrontpageLists
};