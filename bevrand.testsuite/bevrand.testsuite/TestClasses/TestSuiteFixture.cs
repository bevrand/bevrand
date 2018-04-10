using System;
using System.IO;
using bevrand.testsuite.Clients;
using bevrand.testsuite.SettingsObjects;
using Microsoft.Extensions.Configuration;
using OpenQA.Selenium.Remote;

namespace bevrand.testsuite.TestClasses
{
    public class TestSuiteFixture : IDisposable
    {
        private ServiceCalls ServiceCalls { get; }
        public MongoApiClient MongoApi { get; }
        public BaseApiClient BaseApiClient { get; }
        public string AuthenticationUrl { get; }
        public RandomizerApiClient RandomizerApi { get; }
        public string RandomizerUrl { get; }
        public DesiredCapabilities DriverCapabilities { get; }

        public TestSuiteFixture()
        {
            ServiceCalls = new ServiceCalls();
            EnvBuilder();
            BaseApiClient = new BaseApiClient();
            MongoApi = new MongoApiClient(ServiceCalls.MongoApiService);
            RandomizerApi = new RandomizerApiClient();
            RandomizerUrl = ServiceCalls.RandomizerApiService;
            AuthenticationUrl = ServiceCalls.AuthenticationApiService;
            DriverCapabilities = DesiredCapabilities.Chrome();
        }

        private void EnvBuilder()
        {
            var environmentName = "development";

            const string BaseFilePath = @"Settings/";
            dynamic assemblyType = typeof(TestSuiteFixture);
            string assemblyLocation = assemblyType.Assembly.Location;
            var solutionPath = Path.GetDirectoryName(assemblyLocation);
         //   solutionPath = "/home/joerivrij/Projects/bevrand/bevrand.testsuite/bevrand.testsuite";
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