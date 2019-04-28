const express = require('express');
const config = require('../../config');
const { handleLogin, registerUser } = require('../controllers/authentication');
const router = express.Router();

router.post(
  '/login',
  handleLogin(
    config.authenticationApi,
    config.authenticationSecret,
    config.authenticationExpirationTime
  )
);

router.post('/register', registerUser(config.authenticationApi));

module.exports = router;