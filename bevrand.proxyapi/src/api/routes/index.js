const express = require('express');

const router = express.Router();

router.use('/authentication-api', require('./authentication'));
router.use('/highscore-api', require('./highscore'));
router.use('/playlist-api', require('./playlist'));
router.use('/randomize-api', require('./randomizer'));

// Backwards compatibility:
router.use('/api', require('./authentication'));
router.use('/api', require('./highscore'));
router.use('/api', require('./playlist'));
router.use('/api', require('./randomizer'));


module.exports = router;