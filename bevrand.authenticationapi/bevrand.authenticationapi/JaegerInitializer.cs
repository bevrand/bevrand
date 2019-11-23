using Jaeger;
using Jaeger.Samplers;
using Microsoft.Extensions.Logging;

namespace bevrand.authenticationapi
{
    /// <summary>
    /// Initial configuration for Jaeger Client
    /// </summary>
    public static class JaegerInitializer
    {
        /// <summary>
        /// Get configured instance of Jaeger Client 
        /// </summary>
        /// <param name="serviceName">Name of service for which Tracer is configured</param>
        /// <param name="loggerFactory">Logger factory which should be used by Jaeger Client</param>
        /// <returns> Jaeger Client instance</returns>
        public static Tracer Init(string serviceName, ILoggerFactory loggerFactory)
        {
            var samplerConfiguration = new Configuration.SamplerConfiguration(loggerFactory)
                .WithType(ConstSampler.Type)
                .WithParam(1);

            var reporterConfiguration = new Configuration.ReporterConfiguration(loggerFactory)
                .WithSender(Configuration.SenderConfiguration.FromEnv(loggerFactory))
                .WithLogSpans(true);

            return (Tracer)new Configuration(serviceName, loggerFactory)
                .WithSampler(samplerConfiguration)
                .WithReporter(reporterConfiguration)
                .GetTracer();
        }
    }
}