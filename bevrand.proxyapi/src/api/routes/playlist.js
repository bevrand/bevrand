const express = require('express');
const controller = require('../controllers/playlist');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { playlistApi } = require('../../config');
const { validateJwtHeader } = require('../middlewares/jwt');

const router = express.Router();

//TODO: add param validation

router.get('/v2/frontpage', controller.frontpage);

// TODO: only reroute requests with public path to playlistApi
// router.get(/public/, reRouteTo(playlistApi));

// prettier-ignore
router.route(/private/)
  .all(validateJwtHeader)
  .get(controller.playlists)
  .post(reRouteTo(playlistApi, 'playlist-api'))
  .put(reRouteTo(playlistApi, 'playlist-api'))
  .delete(reRouteTo(playlistApi, 'playlist-api'));

router.use(reRouteTo(playlistApi, 'playlist-api'));

module.exports = router;
