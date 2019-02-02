const { initTracer } = require("./jaegerTracer");
const { jaegerAgentHostName } = require('../../config');

module.exports = initTracer('ProxyApi', jaegerAgentHostName);