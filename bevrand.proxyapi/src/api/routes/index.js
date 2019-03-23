const express = require('express');

const router = express.Router();

router.use('/auth', require('./authentication'));
router.use('/highscore', require('./highscore'));
router.use('/playlist', require('./playlist'));
router.use('/randomizer', require('./randomizer'));

// Backwards compatibility:
router.use('/', require('./authentication'));
router.use('/', require('./highscore'));
router.use('/', require('./playlist'));
router.use('/', require('./randomizer'));


module.exports = router;