const express = require('express');
const { reRouteGetTo } = require('../middlewares/reRouteRequest');
const { recommendationApi } = require('../../config');
// const { validateJwtHeader } = require('../middlewares/jwt');

const router = express.Router();

router
  .route('/')
  // .all(validateJwtHeader)
  .get(reRouteGetTo(recommendationApi, 'recommendation-api'));

module.exports = router;
