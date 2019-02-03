const { httpRequest } = require('../lib/tracing/httpRequestWithTracing');
const config = require('../../config/variables');
const { Tags } = require('opentracing');
const tracer = require('../utils/tracing/tracerClass');
const Promise = require('bluebird');
const { signObjectWithJwtToken } = require('../helpers/jwtToken');

exports.getAllPlaylists = async (username, span) => {
  const response = await httpRequest({
    url: `${config.playlistApi}/private/${username}`,
    method: 'GET',
    span,
  });

  span.setTag(Tags.HTTP_STATUS_CODE, 200);

  span.log({
    event: 'playlists-for-user',
    result: result,
  });

  const { result } = JSON.parse(response);

  const playlists = await Promise.all(
    result.map(value => {
      const childSpan = tracer.startSpan('playlist-sub-request', {
        childOf: span,
        tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER },
      });

      return httpRequest({
        url: `${config.playlistApi}/api/v1/private/${username}/${value}`,
        method: 'GET',
        span: childSpan,
      }).then(response => {
        childSpan.setTag(Tags.HTTP_STATUS_CODE, 200);
        childSpan.finish();
        const parsedResponse = JSON.parse(response).result;
        const signedResponse = signObjectWithJwtToken(parsedResponse);
        return signedResponse;
      });
    })
  );

  console.log('Results of promise all: ', playlists);
  span.log({
    event: 'playlists-result',
    result: playlists,
  });

  return { playlists, span };
};
