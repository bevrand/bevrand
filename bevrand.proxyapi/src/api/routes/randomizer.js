const express = require('express');
const router = express.Router();

const { validateJwtTokenMiddleware } = require('./../helpers/jwtToken');
const config = require('../config');

router.post(
  '/v2/randomize',
  validateJwtTokenMiddleware,
  requestRandomizePost(config.randomizerApi)
);

module.exports = { router };
