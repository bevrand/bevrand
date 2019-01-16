const { initTracer: initJaegerTracer } = require("jaeger-client");

module.exports.initTracer = (serviceName, hostName) => {
  const config = {
    serviceName: serviceName,
    sampler: {
      type: "const",
      param: 1,
    },
    reporter: {
      logSpans: true,
      agentHost: hostName
    },
  };
  const options = {
    logger: {
      info(msg) {
        console.log("INFO ", msg);
      },
      error(msg) {
        console.log("ERROR ", msg);
      },
    },
  };
  return initJaegerTracer(config, options);
};
