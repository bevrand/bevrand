const config = require('../config');
const playlistService = require('../services/playlists');
const tracer = require('../lib/tracing/tracerClass');
const { Tags } = require('opentracing');
const { httpRequest } = require('../lib/tracing/httpRequestWithTracing');
const { signObjectWithJwtToken } = require('../helpers/jwtToken');

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

    let newResult = JSON.parse(result).result.map(signObjectWithJwtToken);

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

exports.playlists = async (req, res, next) => {
  const span = tracer.startSpan('playlists-request');

  span.log({
    event: 'playlists-query-parameters',
    result: req.query,
  });

  try {
    // TODO: move to seperate validation
    if (!req.query.username) {
      const invalidParamsError = new Error('Username parameter is missing');
      invalidParamsError.statusCode = 400;
    }

    const playlists = await playlistService.getAllPlaylists(req.query.username, span);
    res.send(playlists);

    span.finish();
  } catch (err) {
    span.setTag(Tags.ERROR, true);
    span.setTag(Tags.HTTP_STATUS_CODE, err.statusCode || 500);
    span.finish();
    return next(err);
  }
};
