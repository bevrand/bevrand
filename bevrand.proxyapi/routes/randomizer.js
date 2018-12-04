const express = require('express');
const router = express.Router();

const { validateJwtTokenMiddleware } = require('./../helpers/jwtToken');
const { httpPostRequest, httpRequest } = require('../lib/tracing/httpRequestWithTracing');
const { Tags } = require('opentracing');
const tracer = require('../lib/tracing/tracerClass');
const config = require('../config');

/**
 * Calls the backend randomize api with POST at endpoint /api/randomize
 * Takes from the post body (req.body) the properties user, list, and beverages.
 * @param {string} endpoint 
 */
const requestRandomizePost = (endpoint) => {
  return (req, res, next) => {
    const { user, list, beverages } = req.body;

    const span = tracer.startSpan('randomize-request');

    span.log({
      event: 'randomize-query-parameters',
      result: req.query
    });
  
    httpPostRequest({
      method: 'POST',
      url: `${endpoint}/api/randomize`,
      qs: req.query,
      body: {
        user,
        list,
        beverages
      },
      span
    }).then((result) => {
      span.setTag(Tags.HTTP_STATUS_CODE, 200);
      span.log({
        event: 'randomize-result',
        result: result
      });
      span.finish();
      return res.send(result);
    }).catch(err => {
      span.setTag(Tags.ERROR, true)
      span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
      span.finish();
      return next(err);
    })
  }
};

router.get('/redis', (req, res, next) => {
  const span = tracer.startSpan('redis-request');
  
  span.log({
    event: 'randomize-query-parameters',
    result: req.query
  });

  httpRequest({
    url: config.randomizerApi + req.originalUrl,
    method: 'GET',
    span
  }).then(result => {
    span.setTag(Tags.HTTP_STATUS_CODE, 200);
    span.log({
      event: 'redis-result',
      result: result
    });
    span.finish();
    return res.send(result);
  }).catch(err => {
    span.setTag(Tags.ERROR, true)
    span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
    span.finish();
    next(err);
  })
});

router.post('/v2/randomize', validateJwtTokenMiddleware, requestRandomizePost(config.randomizerApi));

module.exports = { router }