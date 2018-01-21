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
  MONGO_API: joi.string()
    .required(),
  RANDOMIZER_API: joi.string()
    .required(),
  PORT: joi.any()
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
  mongoApi: envVars.MONGO_API,
  randomizerApi: envVars.MONGO_API,
  server: {
    port: envVars.PORT,
  },
  defaultFrontpageList: envVars.DEFAULT_FRONTPAGE_LIST
}

module.exports = config;