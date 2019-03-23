const express = require('express');
const config = require('../config');
const router = express.Router();
const controller = require('../controllers/highscore');

router.get('/highscore', controller.handleHighscore);

module.exports = { router };