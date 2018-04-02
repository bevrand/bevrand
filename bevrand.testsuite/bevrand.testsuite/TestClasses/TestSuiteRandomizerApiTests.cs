using System.Collections.Generic;
using bevrand.testsuite.Models.RandomizerApi;
using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestSuiteRandomizerApiTests
    {
        private readonly TestSuiteFixture _fixture;
        
        public TestSuiteRandomizerApiTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }

        [Fact]
        [Trait("Category", "Randomizer")]
        public void PostingTwoDrinksReturnsARandomDrink()
        {
            var request = new RandomizePostRequest
            {
                list = "testsuite",
                user = "testsuite",
                beverages = new List<string>
                {
                    "beer",
                    "wine"
                }
            };

            var response = _fixture.RandomizerApi.PostASimpleList(request) as RandomizePostResult;
            
            Assert.Contains(response.beverage, request.beverages);
            Assert.Equal(200, response.statusCode);
        }
        
    }
}