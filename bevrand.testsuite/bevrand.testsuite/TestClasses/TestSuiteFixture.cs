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
        public MongoApiClient MongoApi { get; }
        public RandomizerApiClient RandomizerApi { get; }
        public AuthenticationApiClient AuthenticationApi { get; }
        
        public TestSuiteFixture()
        {
            ServiceCalls = new ServiceCalls();
            EnvBuilder();
            MongoApi = new MongoApiClient(ServiceCalls.MongoApiService);
            RandomizerApi = new RandomizerApiClient(ServiceCalls.RandomizerApiService);
            AuthenticationApi = new AuthenticationApiClient(ServiceCalls.AuthenticationApiService);
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