const express = require('express');
const controller = require('../controllers/playlist');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { playlistApi } = require('../../config');
const { validateJwtHeader } = require('../middlewares/jwt');

const router = express.Router();

//TODO: add param validation

router.get('/v2/frontpage', controller.frontpage);

router.get('/playlists', controller.playlists);

// catch all other route possibilities for this path, and send them directly to playlist api
router.get(/public/, reRouteTo(playlistApi));

// prettier-ignore
router.route(/private/)
  .all(validateJwtHeader)
  .get(controller.playlists)
  .post(reRouteTo(playlistApi))
  .put(reRouteTo(playlistApi))
  .delete(reRouteTo(playlistApi));


module.exports = router;