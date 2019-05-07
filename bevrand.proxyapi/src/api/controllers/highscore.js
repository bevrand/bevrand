const config = require('../../config');
const tracer = require('../utils/tracing/tracerClass');
const { Tags } = require('opentracing');
const { httpRequest } = require('../utils/tracing/httpRequestWithTracing');

const handleHighscore = (req, res, next) => {
  const span = tracer.startSpan('highscore-request');

  span.log({
    event: 'highscore-query-parameters',
    result: req.query,
  });

  httpRequest({
    url: config.highscoreApi + req.originalUrl.replace('highscore-api', 'api'),
    method: 'GET',
    span,
  })
    .then(result => {
      span.setTag(Tags.HTTP_STATUS_CODE, 200);
      span.log({
        event: 'highscore-result',
        result,
      });
      span.finish();
      return res.send(result);
    })
    .catch(err => {
      span.setTag(Tags.ERROR, true);
      span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
      span.finish();
      next(err);
    });
};

module.exports = { handleHighscore };
