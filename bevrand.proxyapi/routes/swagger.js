const express = require("express");
const router = express.Router();

const swaggerUi = require('swagger-ui-express');
const yamljs = require('yamljs');
const swaggerDocument = yamljs.load('swagger.yaml');


router.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

module.exports = { router };