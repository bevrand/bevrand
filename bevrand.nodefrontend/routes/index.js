var express = require('express');
var router = express.Router();
var apiControllers = require('../controllers/frontpage.js');

/* GET front page. */
router.get('/', [
    apiControllers.retrieveFrontpageLists, 
    apiControllers.retrieveFrontpageDefaultList,
    apiControllers.renderFrontpage
]);

module.exports = router;