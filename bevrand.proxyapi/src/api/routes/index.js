const express = require('express');

const router = express.Router();

// TODO: standard definition for each api, replace the standard name with 'api'

router.use('/authentication-api', require('./authentication'));
router.use('/highscore-api', require('./highscore'));
router.use('/ocr-api', require('./ocr'));
router.use('/playlist-api', require('./playlist'));
router.use('/randomize-api', require('./randomizer'));
router.use('/recommendation-api', require('./recommendation'));

// Backwards compatibility:
router.use('/api', require('./authentication'));
router.use('/api', require('./highscore'));
router.use('/api', require('./playlist'));
router.use('/api', require('./randomizer'));

module.exports = router;
