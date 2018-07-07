using System.Collections.Generic;
using AutoMapper.Mappers;
using bevrand.testsuite.Models;
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
            var requeststring = _fixture.RandomizerUrl + "/api/randomize";
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

            var response =
                _fixture.BaseApiClient.GenericPostObject<RandomizePostResult>(requeststring, request).Result as
                    RandomizePostResult;
            
            var drink = response.result;
            Assert.Contains(drink, request.beverages);
            Assert.Equal(200, response.StatusCode);
        }
        
        [Fact]
        [Trait("Category", "Randomizer")]
        public void LongListsGetRandomized()
        {
            var requeststring = _fixture.RandomizerUrl + "/api/randomize";
            var request = new RandomizePostRequest
            {
                list = "testsuite",
                user = "testsuite",
                beverages = new List<string>
                {
                    "drink1",
                    "drink2",
                    "drink3",
                    "drink4",
                    "drink5",
                    "drink6",
                    "drink7",
                    "drink8",
                    "drink9",
                    "drink10",
                    "drink11",
                    "drink12",
                    "drink13",
                    "drink14",
                    "drink15",
                    "drink16",
                    "drink17",
                    "drink18"
                }
            };

            var response =
                _fixture.BaseApiClient.GenericPostObject<RandomizePostResult>(requeststring, request).Result as
                    RandomizePostResult;
            
            var drink = response.result;
            Assert.Contains(drink, request.beverages);
            Assert.Equal(200, response.StatusCode);
        }

        [Fact]
        [Trait("Category", "Randomizer")]
        public void PostASingleDrinkGivesAnError()
        {
            var requeststring = _fixture.RandomizerUrl + "/api/randomize";
            var request = new RandomizePostRequest
            {
                list = "testsuite",
                user = "testsuite",
                beverages = new List<string>
                {
                    "beer"
                }
            };

            var response =
                _fixture.RandomizerApi.PostASampleListWithBeverages(requeststring, request).Result as
                    BaseErrorResponse;
            
            Assert.Equal(400, response.StatusCode);
            Assert.Contains("Errors occured when validating", response.UserError);
        }
        
        [Theory]
        [Trait("Category", "Randomizer")]
        [InlineData(null, null, "null value not allowed")]
        [InlineData(null, "validuser", "null value not allowed")]
        [InlineData("validlist", null, "null value not allowed")]
        [InlineData("e", "validuser", "min length is 2")]
        [InlineData("validlist", "e", "min length is 3")]
        public void PostWithAnInvalidObjectGivesAnError(string list, string user, string message)
        {
            var requeststring = _fixture.RandomizerUrl + "/api/randomize";
            var request = new RandomizePostRequest
            {
                list = list,
                user = user,
                beverages = new List<string>
                {
                    "beer",
                    "wine"
                }
            };

            var response =
                _fixture.RandomizerApi.PostASampleListWithBeverages(requeststring, request).Result as
                    BaseErrorResponse;
            
            Assert.Equal(400, response.StatusCode);
            Assert.Contains(message, response.UserError);
        }

        
    }
}