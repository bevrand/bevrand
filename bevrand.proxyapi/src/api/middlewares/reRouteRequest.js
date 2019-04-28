const request = require('request');

/**
 * Util to pipe requests to another endpoint
 * @param {string} reRouteEndpoint
 */
const reRouteGetTo = reRouteEndpoint => {
  return (req, res) => {
    const url = `${reRouteEndpoint}/api${req.path}`;
    console.log(`# Rereouting to ${url}`);
    req.pipe(request({ qs: req.query, uri: url })).pipe(res);
  };
};

const reRouteTo = reRouteEndpoint => {
  return (req, res) => {
    console.log(`# Rereouting to ${reRouteEndpoint}/api${req.path}`);
    const options = {
      uri: `${reRouteEndpoint}/api${req.path}`,
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
