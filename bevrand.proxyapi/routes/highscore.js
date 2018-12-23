const express = require('express');
const request = require('request');
const router = express.Router();
const config = require('../config');
const jwt = require('jsonwebtoken');
const Promise = require('bluebird');
const { requestPipeGet } = require('../helpers/requestPipes');
const tracer = require('../lib/tracing/tracerClass');
const { Tags } = require('opentracing');
const { httpRequest } = require('../lib/tracing/httpRequestWithTracing');

router.get('/highscore', (req, res, next) => {
  const span = tracer.startSpan('highscore-request');

  span.log({
    event: 'highscore-query-parameters',
    result: req.query
  });

  httpRequest({
    url: config.highScoreApi + req.originalUrl,
    method: 'GET',
    span
  }).then(result => {
    span.setTag(Tags.HTTP_STATUS_CODE, 200);
    span.log({
      event: 'highscore-result',
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


module.exports = { router }