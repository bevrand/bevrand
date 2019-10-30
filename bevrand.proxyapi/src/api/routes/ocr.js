const express = require('express');
const { reRouteTo } = require('../middlewares/reRouteRequest');
const { ocrApi } = require('../../config');
const { validateJwtHeader } = require('../middlewares/jwt');

const router = express.Router();

router.use(validateJwtHeader, reRouteTo(ocrApi, 'ocr-api'));

module.exports = router;
