const express = require('express');
const controller = require('../controllers/highscore');

const router = express.Router();

router.get('/highscore', controller.handleHighscore);

module.exports = router;