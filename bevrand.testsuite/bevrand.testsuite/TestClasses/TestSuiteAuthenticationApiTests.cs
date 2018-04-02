using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestSuiteAuthenticationApiTests
    {
        private readonly TestSuiteFixture _fixture;
        
        public TestSuiteAuthenticationApiTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }
    }
}