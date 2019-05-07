exports.checkAuthorization = (req, res, next) => {
  if (!res.locals.user || !req.path.includes(res.locals.user.username)) {
    const err = new Error('User has no access to this route');
    err.status = 403;

    next(err);
  }

  next();
};
