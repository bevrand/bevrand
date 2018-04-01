const rp = require('request-promise');
const debug = require('debug')('controllers:playlists');

const getFrontpageLists = (mongoApiurl) => {
  return (req, res, next) => {
    rp(`${mongoApiurl}/api/frontpage`)
      .then(result => {
        debug('Got successful result from /frontpagelists: ' + result);
        const parsedResults = JSON.parse(result);
        res.send({ playlists: parsedResults }) 
      })
      .catch(err => {
        debug('Got error from frontpagelists' + err);
        return next(err);
      });
  }
}

const getUserList = (mongoApiurl) => {
  return(req, res, next) => {
    rp(`${mongoApiurl}/api/list?user=${req.query.user}&list=${req.query.list}`)
      .then(result => {
        debug('Got succesful result from / ')
        const parsedResults = JSON.parse(result);
        res.send({ playlists: parsedResults }) 
      })
      .catch(err => {
        debug('Got error from frontpagelists' + err);
        return next(err);
      });
  }
}

module.exports = {
  getFrontpageLists: getFrontpageLists,
  getUserList: getUserList
};