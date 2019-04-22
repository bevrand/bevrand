const jwt = require('jsonwebtoken');
const { Tags } = require('opentracing');
const { httpPostRequest, httpRequest } = require('../utils/tracing/httpRequestWithTracing');
const tracer = require('../utils/tracing/tracerClass');

function handleLogin(authenticationUrl, secret, expirationTime) {
  return async (req, res, next) => {
    const span = tracer.startSpan('login-request');

    span.log({
      event: 'login-query-parameters',
      result: req.query,
    });

    try {
      const token = await getAuthToken({
        span,
        authenticationUrl,
        secret,
        expirationTime,
        body: req.body,
      });

      span.log({
        event: 'login-result',
        result: 'Succesfully authenticated User',
      });
      span.finish();

      return res.send({
        success: true,
        message: 'Succesfully authenticated User',
        token: token,
      });
    } catch (err) {
      span.setTag(Tags.ERROR, true);
      span.setTag(Tags.HTTP_STATUS_CODE, err.status);
      span.finish();

      next(err);
    }
  };
}

async function getAuthToken({ span, authenticationUrl, body, secret, expirationTime }) {
  const validationSpan = tracer.startSpan('login-validation-request', {
    childOf: span,
    tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER },
  });

  const isValidLogin = await httpPostRequest({
    method: 'POST',
    url: `${authenticationUrl}/api/Validate`,
    body: body,
    json: true,
    simple: false,
    span: validationSpan,
  });

  if (!isValidLogin) {
    let authenticationError = new Error('Username or password is incorrect');
    authenticationError.status = 401;
    validationSpan.setTag(Tags.ERROR, true);
    validationSpan.setTag(Tags.HTTP_STATUS_CODE, authenticationError.status);
    validationSpan.finish();
    throw authenticationError;
  }

  validationSpan.setTag(Tags.HTTP_STATUS_CODE, 200);
  validationSpan.finish();

  // Is authenitcationExpirationTime a number?
  const user = await fetchUserObject(authenticationUrl, body);
  const token = jwt.sign(
    { id: user.id, username: user.username, email: user.emailAddress },
    secret,
    {
      expiresIn: expirationTime,
    }
  );

  return token;
}

async function fetchUserObject(authenticationUrl, body) {
  const requestRoute = !body.username
    ? `by-email/${body.emailAddress}`
    : `by-username/${body.username}`;

  const user = await httpRequest({
    method: 'GET',
    url: `${authenticationUrl}/api/Users/${requestRoute}`,
  });

  return JSON.parse(user);
}

function registerUser(authenticationUrl) {
  return async (req, res, next) => {
    const { username, password, emailAddress } = req.body;

    const span = tracer.startSpan('login-request');

    span.log({
      event: 'login-query-parameters',
      result: req.query,
    });

    try {
      if (!username || !password || !emailAddress) {
        let validationError = new Error('Required body elements are not present');
        validationError.status = 400;
        span.setTag(Tags.ERROR, true);
        span.setTag(Tags.HTTP_STATUS_CODE, validationError.status);
        span.finish();
        throw validationError;
      }

      const result = await httpPostRequest({
        method: 'POST',
        url: `${authenticationUrl}/api/Users`,
        body: req.body,
        json: true,
        span,
      });

      span.setTag(Tags.HTTP_STATUS_CODE, 200);
      span.finish();

      res.send(result);
    } catch (err) {
      span.setTag(Tags.ERROR, true);
      span.setTag(Tags.HTTP_STATUS_CODE, err.status);
      span.finish();
      next(err);
    }
  };
}

module.exports = {
  handleLogin,
  registerUser,
};
