const request = require('request')

/**
 * Util to pipe requests to another endpoint
 * @param {string} endpoint 
 */
const requestPipeGet = (endpoint) => {
    return (req, res) => {
        const url = endpoint + req.url;
        req.pipe(request({ qs: req.query, uri: url })).pipe(res);
    }
}

/**
 * Util to pipe requests to another endpoint
 * Also pipes the post body
 * @param {string} endpoint 
 */
const requestPipePost = (endpoint) => {
    return (req, res) => {
        request({
            method: 'POST',
            qs: req.query,
            uri: endpoint + req.url,
            body: req.body,
            json: true
        }).pipe(res);
    }
}

module.exports = { requestPipeGet, requestPipePost}