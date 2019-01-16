const express = require('express');
const router = express.Router();
const config = require('../config');
const exjwt = require('express-jwt');

const jwtMW = exjwt({
  secret: config.authenticationSecret
});

router.get('/test/validateJWT', jwtMW, (req, res)=> {
  res.send('You are authenticated');
});

module.exports = { router };