const request = require('request');

const requestPath = (apiName, path) => (apiName ? path.replace(apiName, 'api') : path);

/**
 * Util to pipe requests to another endpoint
 * @param {string} reRouteEndpoint
 */
const reRouteGetTo = (reRouteEndpoint, apiName) => {
  return (req, res) => {
    const url = reRouteEndpoint + requestPath(apiName, req.path);
    console.log(`# Rereouting to ${url}`);
    req.pipe(request({ qs: req.query, uri: url })).pipe(res);
  };
};

const reRouteTo = (reRouteEndpoint, apiName) => {
  return (req, res) => {
    console.log(`# Rereouting to ${reRouteEndpoint}${req.path}`);
    const options = {
      uri: reRouteEndpoint + requestPath(apiName, req.path),
      method: req.method,
      qs: req.query,
    };

    if (req.body) {
      options.body = req.body;
      options.json = true;
    }

    request(options).pipe(res);
  };
};

module.exports = { reRouteTo, reRouteGetTo };
