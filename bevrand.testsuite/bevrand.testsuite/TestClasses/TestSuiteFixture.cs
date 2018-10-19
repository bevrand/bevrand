using System;
using System.IO;
using bevrand.testsuite.Clients;
using bevrand.testsuite.SettingsObjects;
using Microsoft.Extensions.Configuration;

namespace bevrand.testsuite.TestClasses
{
    public class TestSuiteFixture : IDisposable
    {
        private ServiceCalls ServiceCalls { get; }
        public BaseApiClient BaseApiClient { get; }
        public string AuthenticationUrl { get; }
        public string PlayListUrl { get; }
        public string ProxyUrl { get; }
        public RandomizerApiClient RandomizerApi { get; }
        public string RandomizerUrl { get; }

        public TestSuiteFixture()
        {
            ServiceCalls = new ServiceCalls();
            EnvBuilder();
            BaseApiClient = new BaseApiClient();
            PlayListUrl = ServiceCalls.PlayListApiService;
            ProxyUrl = ServiceCalls.ProxyApiService;
            RandomizerApi = new RandomizerApiClient();
            RandomizerUrl = ServiceCalls.RandomizerApiService;
            AuthenticationUrl = ServiceCalls.AuthenticationApiService;
        }

        private void EnvBuilder()
        {
            var environmentName = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT");
            Console.WriteLine(environmentName);
                
            const string BaseFilePath = @"Settings/";
            var assemblyType = typeof(TestSuiteFixture);
            var assemblyLocation = assemblyType.Assembly.Location;
            var solutionPath = Path.GetDirectoryName(assemblyLocation);
            var settingsPath = Path.Combine(solutionPath, BaseFilePath);


            var builder = new ConfigurationBuilder()
                .SetBasePath(
                    settingsPath)
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .AddJsonFile($"appsettings.{environmentName}.json", optional: true);
            var root = builder.Build();

            root.GetSection("ServiceCalls").Bind(ServiceCalls);
        }

        public void Dispose()
        {
        }
    }
}