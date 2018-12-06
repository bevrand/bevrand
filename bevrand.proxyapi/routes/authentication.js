const jwt = require('jsonwebtoken');
const express = require('express');
const config = require('../config');
const router = express.Router();

const { httpPostRequest, httpRequest } = require('../lib/tracing/httpRequestWithTracing');
const { Tags } = require('opentracing');
const tracer = require('../lib/tracing/tracerClass');

const handleLogin = (authenticationUrl, secret, expirationTime) => {
  return async (req, res, next) => {
    //TODO: seperate clients for every other api
    const { userName, passWord, emailAddress } = req.body;

    const span = tracer.startSpan('login-request');

    span.log({
      event: 'login-query-parameters',
      result: req.query
    });

    if (!(userName || emailAddress) || !passWord) {
      let err = new Error('Required body elements are not present');
      err.status = 400;

      return next(err);
    }

    try {
      const validationSpan = tracer.startSpan('login-validation-request', {
        childOf: span,
        tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER }
      });
      const result = await httpPostRequest({
        method: 'POST',
        url: `${authenticationUrl}/api/Validate`,
        body: req.body,
        json: true,
        span: validationSpan
      })
      if (!result) {
        let authenticationError = new Error('Username or password is incorrect');
        authenticationError.status = 401;
        validationSpan.setTag(Tags.ERROR, true)
        validationSpan.setTag(Tags.HTTP_STATUS_CODE, authenticationError.status);
        validationSpan.finish();
        throw authenticationError;
      }

      validationSpan.setTag(Tags.HTTP_STATUS_CODE, 200);
      validationSpan.finish();


      const retrieveUserSpan = tracer.startSpan('login-retrieveUser-request', {
        childOf: span,
        tags: { [Tags.SPAN_KIND]: Tags.SPAN_KIND_RPC_SERVER }
      });
      const user = await httpRequest({
        method: 'GET',
        url: `${authenticationUrl}/api/Users/by-username/${userName}`,
        span: retrieveUserSpan
      });

      const { active, id } = JSON.parse(user);
      if (!active) {
        let inActiveUserError = new Error("User is not active");
        inActiveUserError.status = 403;
        retrieveUserSpan.setTag(Tags.ERROR, true)
        retrieveUserSpan.setTag(Tags.HTTP_STATUS_CODE, inActiveUserError.status);
        retrieveUserSpan.finish();
        throw inActiveUserError;
      }
      retrieveUserSpan.setTag(Tags.HTTP_STATUS_CODE, 200);
      retrieveUserSpan.finish();

      // Is authenitcationExpirationTime a number?
      let token = jwt.sign({ id: id, username: userName }, secret, { expiresIn: expirationTime });
      span.log({
        event: 'login-result',
        result: 'Succesfully authenticated User'
      })
      span.finish();
      return res.send({
        success: true,
        message: 'Succesfully authenticated User',
        token: token
      })
    } catch (err) {
      span.setTag(Tags.ERROR, true);
      span.setTag(Tags.HTTP_STATUS_CODE, err.status);
      span.finish()
      next(err);
    }
  }
}

const registerUser = (authenticationUrl) => {
  return async (req, res, next) => {
    const { userName, passWord, emailAddress } = req.body;

    const span = tracer.startSpan('login-request');

    span.log({
      event: 'login-query-parameters',
      result: req.query
    });

    try {
      if (!userName || !passWord || !emailAddress) {
        let validationError = new Error('Required body elements are not present');
        validationError.status = 400;
        span.setTag(Tags.ERROR, true)
        span.setTag(Tags.HTTP_STATUS_CODE, validationError.status);
        span.finish();
        throw validationError
      }

      const result = await httpPostRequest({
        method: 'POST',
        url: `${authenticationUrl}/api/Users`,
        body: req.body,
        json: true,
        span
      });

      span.setTag(Tags.HTTP_STATUS_CODE, 200);
      span.finish();

      res.send(result);
    } catch (err) {
      span.setTag(Tags.ERROR, true)
      span.setTag(Tags.HTTP_STATUS_CODE, err.status);
      span.finish();
      next(err);
    }
  }
}

router.post('/login',
  handleLogin(
    config.authenticationApi,
    config.authenticationSecret,
    config.authenticationExpirationTime
  )
);

router.post('/register',
  registerUser(config.authenticationApi)
);

module.exports = {
  router,
  handleLogin,
  registerUser
};