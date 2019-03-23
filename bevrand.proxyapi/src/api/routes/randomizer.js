const express = require('express');
const { validateJwtTokenMiddleware } = require('./../helpers/jwtToken');
const config = require('../config');
const controller = require('../controllers/randomizer');

const router = express.Router();

router.post(
  '/v2/randomize',
  validateJwtTokenMiddleware,
  controller.requestRandomizePost(config.randomizerApi)
);

module.exports = router;
