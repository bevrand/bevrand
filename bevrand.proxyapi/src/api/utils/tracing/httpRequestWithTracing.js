const request = require('request-promise');
const { Tags, FORMAT_HTTP_HEADERS } = require('opentracing');
const tracer = require('./tracerClass');

async function httpRequest({ url, method = 'GET', span, simple = true, qs }) {
  const headers = {};

  if (span) {
    span.setTag(Tags.HTTP_URL, url);
    span.setTag(Tags.HTTP_METHOD, method);

    tracer.inject(span, FORMAT_HTTP_HEADERS, headers);
  }

  return request({
    headers,
    method,
    qs,
    simple,
    uri: url,
  });
}

async function httpPostRequest({ url, method, span, simple = true, body }) {
  const headers = {};

  if (span) {
    span.setTag(Tags.HTTP_URL, url);
    span.setTag(Tags.HTTP_METHOD, method);

    tracer.inject(span, FORMAT_HTTP_HEADERS, headers);
  }

  return request({
    headers,
    method,
    uri: url,
    body,
    simple,
    json: true,
  });
}

module.exports = { httpRequest, httpPostRequest };
