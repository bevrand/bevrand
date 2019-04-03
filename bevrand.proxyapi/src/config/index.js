const joi = require('joi');

/**
 * Load in Config based on NODE_ENV
 */
// TODO: make it possible to run with just a .env file
if (process.env.NODE_ENV === 'production') {
  require('dotenv').config({ path: './src/config/.production.env' });
} else if (process.env.NODE_ENV === 'development') {
  require('dotenv').config({ path: './src/config/.development.env' });
} else {
  require('dotenv').config({ path: './src/config/.local.env' });
}

/**
 * environment variables schema
 */
const envVarsSchema = joi
  .object({
    PLAYLIST_API: joi.string().required(),
    RANDOMIZER_API: joi.string().required(),
    HIGHSCORE_API: joi.string().required(),
    RECOMMENDATION_API: joi.string().required(),
    AUTHENTICATION_API: joi.string().required(),
    AUTHENTICATION_SECRET: joi.string().required(),
    AUTHENTICATION_EXPIRATION_TIME: joi.number().required(),
    FRONTEND_JWT_SECRET: joi.string().required(),
    PORT: joi
      .any()
      .optional()
      .default(5000),
    USEMOCK: joi.boolean().optional(),
    DEFAULT_FRONTPAGE_LIST: joi.string().optional(),
    JAEGER_AGENT_HOST: joi.string().optional(),
    JAEGER_AGENT_PORT: joi.number().default(),
  })
  .unknown(true);

const { error, value: envVars } = joi.validate(process.env, envVarsSchema);
if (error) {
  throw new Error(`Config validation error: ${error.message}`);
}

const config = {
  playlistApi: envVars.PLAYLIST_API,
  randomizerApi: envVars.RANDOMIZER_API,
  highscoreApi: envVars.HIGHSCORE_API,
  recommendationApi: envVars.RECOMMENDATION_API,
  authenticationApi: envVars.AUTHENTICATION_API,
  authenticationSecret: envVars.AUTHENTICATION_SECRET,
  authenticationExpirationTime: envVars.AUTHENTICATION_EXPIRATION_TIME,
  frontendJwtSecret: envVars.FRONTEND_JWT_SECRET,
  useMock: envVars.USEMOCK,
  server: {
    port: envVars.PORT,
    env: envVars.NODE_ENV || 'local',
  },
  defaultFrontpageList: envVars.DEFAULT_FRONTPAGE_LIST,
  jaegerAgentHostName: envVars.JAEGER_AGENT_HOST || 'localhost',
  jaegerAgentPort: envVars.JAEGER_AGENT_PORT || 6831,
};

module.exports = config;
