const joi = require('joi');

/**
 * Load in Config based on NODE_ENV
 */
if (process.env.NODE_ENV === 'production') {
  require('dotenv').config({ path: './api/config/.production.env' });
} else {
  require('dotenv').config({ path: './api/config/.development.env' });
}

/**
 * environment variables schema
 */
const envVarsSchema = joi.object({
  PLAYLIST_API: joi.string()
    .required(),
  RANDOMIZER_API: joi.string()
    .required(),
  AUTHENTICATION_API: joi.string()
    .required(),
  AUTHENTICATION_SECRET: joi.string()
    .required(),
  AUTHENTICATION_EXPIRATION_TIME: joi.number()
    .required(),
  PORT: joi.any()
    .optional(),
  USEMOCK: joi.boolean()
    .optional(),
  DEFAULT_FRONTPAGE_LIST: joi.string()
    .optional()
}).unknown(true);

const { error, value: envVars } = joi.validate(process.env, envVarsSchema)
if (error) {
  throw new Error(`Config validation error: ${error.message}`);
}

const config = {
  env: envVars.NODE_ENV || 'development',
  playlistApi: envVars.PLAYLIST_API,
  randomizerApi: envVars.RANDOMIZER_API,
  authenticationApi: envVars.AUTHENTICATION_API,
  authenticationSecret: envVars.AUTHENTICATION_SECRET,
  authenticationExpirationTime: envVars.AUTHENTICATION_EXPIRATION_TIME,
  useMock: envVars.USEMOCK,
  server: {
    port: envVars.PORT,
  },
  defaultFrontpageList: envVars.DEFAULT_FRONTPAGE_LIST
}

module.exports = config;