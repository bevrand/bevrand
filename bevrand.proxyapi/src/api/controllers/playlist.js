const config = require('../../config');
const tracer = require('../utils/tracing/tracerClass');
const { Tags } = require('opentracing');
const { httpRequest } = require('../utils/tracing/httpRequestWithTracing');
const { signObject } = require('../services/jwtTokens');

/**
 * Gives the complete response from the playlist api at the endpoint /api/frontpage,
 * signed with a JWT Token, IssuedAtTime property (iat) and a JWT Header, which describes the algorithm used.
 */
exports.frontpage = async (req, res, next) => {
  const span = tracer.startSpan('frontpage-request');

  span.log({
    event: 'frontpage-query-parameters',
    result: req.query,
  });

  try {
    const result = await httpRequest({
      method: 'GET',
      url: `${config.playlistApi}/api/v1/public`,
      span,
    });

    span.setTag(Tags.HTTP_STATUS_CODE, 200);

    let newResult = JSON.parse(result).result.map(signObject);

    span.log({
      event: 'frontpage-result',
      result: newResult,
    });

    span.finish();
    return res.send(newResult);
  } catch (err) {
    span.setTag(Tags.ERROR, true);
    span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
    span.finish();
    return next(err);
  }
};
