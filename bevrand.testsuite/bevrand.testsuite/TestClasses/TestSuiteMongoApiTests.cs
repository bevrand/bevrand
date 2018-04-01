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
        
        [Fact]
        [Trait("Category", "MongoApi")]
        public void FrontPageList()
        {
            var response = _fixture.MongoApi.FrontPageGetWithoutList();
            
            Assert.Equal(200, response.statusCode);

        }
    }
}