using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestsSuiteRandomizerApiTests
    {
        private readonly TestSuiteFixture _fixture;
        
        public TestsSuiteRandomizerApiTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }
        
    }
}