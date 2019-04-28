const express = require('express');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { highscoreApi } = require('../../config');

const router = express.Router();

router.use(reRouteTo(highscoreApi, 'highscore-api'));

module.exports = router;
