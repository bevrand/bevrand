const errorHandler = (err, req, res, next) => {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') !== 'production' ? err : {};

  // Only log when not in production env
  if (req.app.get('env') !== 'production') {
    /* eslint-disable no-console */
    console.error(err);
  }

  // Send the error response object
  let responseStatus = err.status || err.statusCode || 500;
  res.status(responseStatus).send({
    result: 'error',
    message: err.message,
    httpstatus: responseStatus,
  });
};

const setHttpStatus = (err, req, res, next) => {
  if (err.name === 'InvalidJwtToken') {
    err.status = 400;
  } else if (err.name === 'UnauthorizedError') {
    err.status = 401;
  }
  next(err);
};

const notFoundHandler = (req, res, next) => {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
};


module.exports = { errorHandler, setHttpStatus, notFoundHandler };