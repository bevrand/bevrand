const express = require('express');
const request = require('request');
const router = express.Router();
const config = require('../config');
const Promise = require('bluebird');
const { requestPipeGet } = require('../helpers/requestPipes');
const tracer = require('../lib/tracing/tracerClass');
const { Tags } = require('opentracing');
const { httpRequest } = require('../lib/tracing/httpRequestWithTracing');
const { signObjectWithJwtToken } = require('../helpers/jwtToken');


/**
 * Gives the complete response from the playlist api at the endpoint /api/frontpage, 
 * signed with a JWT Token, IssuedAtTime property (iat) and a JWT Header, which describes the algorithm used.
 */
router.get('/v2/frontpage', (req, res, next) => {
  const span = tracer.startSpan('frontpage-request');

  span.log({
    event: 'frontpage-query-parameters',
    result: req.query
  });

  httpRequest({
    method: 'GET',
    url: `${config.playlistApi}/api/v1/public`,
    span
  }).then(result => {
    span.setTag(Tags.HTTP_STATUS_CODE, 200);

    let newResult = JSON.parse(result).result.map(signObjectWithJwtToken);

    span.log({
      event: 'frontpage-result',
      result: newResult
    });

    span.finish()
    return res.send(newResult);
  }).catch(err => {
    span.setTag(Tags.ERROR, true)
    span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
    span.finish();
    return next(err);
  });
});

router.get('/playlists', (req, res, next) => {
  const span = tracer.startSpan('playlists-request');

  span.log({
    event: 'playlists-query-parameters',
    result: req.query
  });

  const { username } = req.query;
  if (!username) {
    let err = new Error('Required parameters are not present');
    err.status = 400;
    return next(err);
  }

  httpRequest({
    url: `${config.playlistApi}/api/v1/private/${username}`,
    method: 'GET',
    span
  }).then(result => {
    let parsedResult = JSON.parse(result).result;
    console.log(parsedResult);
    return parsedResult;
  })
    .then(result => {
      let promises = result.map(value => {
        const childSpan = tracer.startSpan('playlist-sub-request', {
          childOf: span,
          tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER }
        });

        return httpRequest({
          url: `${config.playlistApi}/api/v1/private/${username}/${value}`,
          method: 'GET',
          span: childSpan
        }).then(response => {
          childSpan.setTag(Tags.HTTP_STATUS_CODE, 200);
          childSpan.finish();
          const parsedResponse = JSON.parse(response).result;
          const signedResponse = signObjectWithJwtToken(parsedResponse);
          return signedResponse;
        });
      });

      Promise.all(promises).then(results => {
        console.log('Results of promise all: ', results);
        span.log({
          event: 'playlists-result',
          result: results
        });
        span.finish();
        res.send(results);
      })
    })
    .catch(err => {
      return next(err);
    });
});

/**
* Calls the backend playlist api with POST at endpoint /api/v1/private/{username}
* Takes from the post body (req.body) the properties user, list, and beverages.
* @param {string} endpoint
*/
const requestUserPlaylistPost = (endpoint) => {
  return (req, res) => {
    const { beverages, imageUrl, displayName } = req.body;
    request({
      method: 'POST',
      uri: endpoint + `/api/v1/private/${req.body.user}/${req.body.list}`,
      body: {
        beverages,
        imageUrl,
        displayName
      },
      json: true
    }).pipe(res);
  }
};

router.post('/user', requestUserPlaylistPost(config.playlistApi));

router.get('/user', requestPipeGet(config.playlistApi));




module.exports = { router };