const jwt = require('jsonwebtoken');
const { Tags } = require('opentracing');
const { httpPostRequest, httpRequest } = require('../utils/tracing/httpRequestWithTracing');
const tracer = require('../utils/tracing/tracerClass');

const handleLogin = (authenticationUrl, secret, expirationTime) => {
  return async (req, res, next) => {
    //TODO: seperate clients for every other api
    const { username, password, emailAddress } = req.body;

    let userObject;

    const span = tracer.startSpan('login-request');

    span.log({
      event: 'login-query-parameters',
      result: req.query,
    });

    if (!(username || emailAddress) || !password) {
      let err = new Error('Required body elements are not present');
      err.status = 400;

      return next(err);
    }

    const retrieveUserSpan = tracer.startSpan('login-retrieveUser-request', {
      childOf: span,
      tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER },
    });

    // Retrieve either userName or emailAddress before validating
    // TODO: add error handling
    if (!username) {
      userObject = await httpRequest({
        method: 'GET',
        url: `${authenticationUrl}/api/Users/by-email/${emailAddress}`,
        span: retrieveUserSpan,
      });
    }

    if (!emailAddress) {
      userObject = await httpRequest({
        method: 'GET',
        url: `${authenticationUrl}/api/Users/by-username/${username}`,
        span: retrieveUserSpan,
      });
    }

    const user = JSON.parse(userObject);

    if (!user.active) {
      let inActiveUserError = new Error('User is not active');
      inActiveUserError.status = 403;
      retrieveUserSpan.setTag(Tags.ERROR, true);
      retrieveUserSpan.setTag(Tags.HTTP_STATUS_CODE, inActiveUserError.status);
      retrieveUserSpan.finish();
      next(inActiveUserError);
    }

    retrieveUserSpan.setTag(Tags.HTTP_STATUS_CODE, 200);
    retrieveUserSpan.finish();

    try {
      const validationSpan = tracer.startSpan('login-validation-request', {
        childOf: span,
        tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER },
      });

      const result = await httpPostRequest({
        method: 'POST',
        url: `${authenticationUrl}/api/Validate`,
        body: user,
        json: true,
        span: validationSpan,
      });

      if (!result) {
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
      let token = jwt.sign(
        { id: user.id, username: user.username, email: user.emailAddress },
        secret,
        {
          expiresIn: expirationTime,
        }
      );
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
};

const registerUser = authenticationUrl => {
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
};

module.exports = {
  handleLogin,
  registerUser,
};
