const express = require('express');
const config = require('../../config');
const controller = require('../controllers/randomizer');
const jwtMiddleware = require('../middlewares/jwt');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { validateJwtHeader } = require('../middlewares/jwt');

const router = express.Router();

//router.post('/v2/randomize', controller.requestRandomizePost(config.randomizerApi));
router.post('/v2/randomize', jwtMiddleware.validateJwtInBody, controller.requestRandomizePost(config.randomizerApi));

router.route('/v1/randomize')
  .all(validateJwtHeader)
  .post(reRouteTo(config.randomizerApi, 'randomize-api'));

module.exports = router;
