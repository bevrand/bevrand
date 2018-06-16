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
        public AuthenticationApiClient AuthenicationApi { get; }
        public string AuthenticationUrl { get; }
        public RandomizerApiClient RandomizerApi { get; }
        public string RandomizerUrl { get; }
        public DesiredCapabilities DriverCapabilities { get; }
        public string SeleniumHubUrl { get; }

        public TestSuiteFixture()
        {
            ServiceCalls = new ServiceCalls();
            EnvBuilder();
            BaseApiClient = new BaseApiClient();
            MongoApi = new MongoApiClient(ServiceCalls.MongoApiService);
            RandomizerApi = new RandomizerApiClient();
            RandomizerUrl = ServiceCalls.RandomizerApiService;
            AuthenicationApi = new AuthenticationApiClient();
            AuthenticationUrl = ServiceCalls.AuthenticationApiService;
            DriverCapabilities = DesiredCapabilities.Chrome();
            SeleniumHubUrl = ServiceCalls.SeleniumHubService;
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