const express = require('express');
const controller = require('../controllers/playlist');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { playlistApi } = require('../../config');
const { checkAuthorization } = require('../middlewares/authorization');
const { validateJwtHeader } = require('../middlewares/jwt');

const router = express.Router();

router.get('/v2/frontpage', controller.frontpage);

// prettier-ignore
router.route(/private/)
  .all(validateJwtHeader)
  .all(checkAuthorization)
  .get(reRouteTo(playlistApi, 'playlist-api'))
  .post(reRouteTo(playlistApi, 'playlist-api'))
  .put(reRouteTo(playlistApi, 'playlist-api'))
  .delete(reRouteTo(playlistApi, 'playlist-api'));

router.use(reRouteTo(playlistApi, 'playlist-api'));

module.exports = router;
