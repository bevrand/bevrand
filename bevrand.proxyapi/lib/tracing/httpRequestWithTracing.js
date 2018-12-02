const request = require('request-promise');
const { Tags, FORMAT_HTTP_HEADERS } = require('opentracing');
const tracer = require('./tracerClass');

function httpRequest({url, method, span}) {
  const headers = {};

  span.setTag(Tags.HTTP_URL, url);
  span.setTag(Tags.HTTP_METHOD, method);

  tracer.inject(span, FORMAT_HTTP_HEADERS, headers);
  
  return request({
    headers,
    method,
    uri: url
  })
}

function httpPostRequest({url, method, span, body}) {
  const headers = {};

  span.setTag(Tags.HTTP_URL, url);
  span.setTag(Tags.HTTP_METHOD, method);

  tracer.inject(span, FORMAT_HTTP_HEADERS, headers);

  return request({
    headers,
    method,
    uri: url,
    body,
    json: true
  })
}

module.exports = { httpRequest, httpPostRequest };