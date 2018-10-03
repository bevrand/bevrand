using Xunit;

namespace bevrand.testsuite.TestClasses
{
    
    [Collection("TestSuite Collection")]
    public class TestSuiteProxyApiTests
    {
        private readonly TestSuiteFixture _fixture;
        
        public TestSuiteProxyApiTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }
        
    }
}