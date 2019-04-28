const { httpPostRequest } = require('../utils/tracing/httpRequestWithTracing');
const { Tags } = require('opentracing');
const tracer = require('../utils/tracing/tracerClass');

/**
 * Calls the backend randomize api with POST at endpoint /api/randomize
 * Takes from the post body (req.body) the properties user, list, and beverages.
 * @param {string} endpoint
 */
const requestRandomizePost = endpoint => {
  return (req, res, next) => {
    const { user, list, beverages } = req.body;
    const span = tracer.startSpan('randomize-request');

    span.log({
      event: 'randomize-query-parameters',
      result: req.query,
    });

    httpPostRequest({
      method: 'POST',
      url: `${endpoint}/api/v1/randomize`,
      qs: req.query,
      body: {
        user,
        list,
        beverages,
      },
      span,
    }).then(result => {
      span.setTag(Tags.HTTP_STATUS_CODE, 200);
      span.log({
        event: 'randomize-result',
        result: result,
      });
      span.finish();
      return res.send(result);
    }).catch(err => {
      span.setTag(Tags.ERROR, true);
      span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
      span.finish();
      return next(err);
    });
  };
};

module.exports = { requestRandomizePost }