using bevrand.testsuite.Helpers;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.MongoApi;
using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestSuiteMongoApiTests
    {
        private readonly TestSuiteFixture _fixture;
        
        
        public TestSuiteMongoApiTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }

        /// <summary>
        /// This test should return a specific list which has been queried
        /// </summary>
        [Fact]
        [Trait("Category", "MongoApi")]
        public void FrontPage()
        {
            var request = new RequestString
            {
                list = "tgif"
            };

            var requestString = CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
            var response = _fixture.MongoApi.FrontPageGetWithList(requestString);
            
            Assert.Equal(200, response.statusCode);
            Assert.Equal(request.list, response.list);
            Assert.NotEmpty(response.beverages);
        }
        
        /// <summary>
        /// This test should return a list of all frontpage lists
        /// </summary>
        [Fact]
        [Trait("Category", "MongoApi")]
        public void FrontPageList()
        {
            var response = _fixture.MongoApi.FrontPageGetWithoutList();
            
            Assert.Equal(200, response.statusCode);

        }

        /// <summary>
        /// All lists returned should give a 200 and have data
        /// </summary>
        [Fact]
        [Trait("Category", "MongoApi")]
        public void FrontPageListsAllWork()
        {
            var response = _fixture.MongoApi.FrontPageGetWithoutList();
            
            Assert.Equal(200, response.statusCode);

            foreach (var resp in response.listOfFrontPages)
            {
                var request = new RequestString
                {
                    list = resp.list
                };

                var requestString = CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
                var innerResult = _fixture.MongoApi.FrontPageGetWithList(requestString);
            
                Assert.Equal(200, response.statusCode);
                Assert.Equal(request.list, innerResult.list);
                Assert.NotEmpty(innerResult.beverages);
            }
        }
        
        [Fact]
        [Trait("Category", "MongoApi")]
        public void UsersList()
        {
            var response = _fixture.MongoApi.GetUsers();
            
            Assert.Equal(200, response.statusCode);

        }
        
    }
}