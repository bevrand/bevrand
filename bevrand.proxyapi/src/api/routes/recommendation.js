const express = require('express');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { recommendationApi } = require('../../config');

const router = express.Router();

router.use(reRouteTo(recommendationApi, 'recommendation-api'));

module.exports = router;
