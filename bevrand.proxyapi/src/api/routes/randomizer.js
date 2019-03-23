const express = require('express');
const config = require('../../config');
const controller = require('../controllers/randomizer');

const router = express.Router();

router.post('/v2/randomize', controller.requestRandomizePost(config.randomizerApi));

module.exports = router;
