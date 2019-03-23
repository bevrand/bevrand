const express = require('express');

const router = express.Router();

router.use('/auth', require('./authentication'));
router.use('/highscore', require('./highscore'));
router.use('/playlist', require('./playlist'));
router.use('/randomizer', require('./randomizer'));


module.exports = router;