using bevrand.testsuite.Helpers;
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
            var response = _fixture.MongoApi.FrontPageGetWithList(requestString) as FrontpageResponse;
            
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
            var response = _fixture.MongoApi.FrontPageGetWithoutList() as FrontPageListResponse;
            
            Assert.Equal(200, response.statusCode);

            foreach (var resp in response.listOfFrontPages)
            {
                var request = new RequestString
                {
                    list = resp.list
                };

                var requestString = CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
                var innerResult = _fixture.MongoApi.FrontPageGetWithList(requestString) as FrontpageResponse;
            
                Assert.Equal(200, innerResult.statusCode);
                Assert.Equal(request.list, innerResult.list);
                Assert.NotEmpty(innerResult.beverages);
            }
        }
        
        /// <summary>
        /// Test with a random guid that should throw a 404
        /// </summary>
        [Theory]
        [Trait("Category", "MongoApi")]
        [InlineData("Gsdfkjsdfijksjfe", 404, "The frontpagelist you queried does not exist")]
        [InlineData(" ", 400, "min length is 2")]
        public void FrontPageListThatDoesNotExistsReturnsAnErrir(string list, int errorcode, string errormessage)
        {
            var request = new RequestString
            {
                list = list
            };
            
            var requestString = CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
            var response = _fixture.MongoApi.FrontPageGetWithList(requestString) as ErrorModel;
            Assert.Equal(errorcode, response.statusCode);
            Assert.Contains(errormessage, response.message);
        }

        /// <summary>
        /// Tests that all users are returned
        /// </summary>
        [Fact]
        [Trait("Category", "MongoApi")]
        public void UsersList()
        {
            var response = _fixture.MongoApi.GetUsers() as UsersResponse;
            
            Assert.Equal(200, response.statusCode);
            Assert.NotEmpty(response.ActiveUsers); 

        }
        
        [Fact]
        [Trait("Category", "MongoApi")]
        public void UserListWithEachUser()
        {
            var response = _fixture.MongoApi.GetUsers() as UsersResponse;
            
            Assert.Equal(200, response.statusCode);
            Assert.NotEmpty(response.ActiveUsers); 
            
            
            foreach (var user in response.ActiveUsers)
            {
                var request = new RequestString
                {
                    user = user
                };

                var requestString = CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
                var innerResult = _fixture.MongoApi.GetUser(requestString) as UserResponse;
            
                Assert.Equal(200, innerResult.statusCode);
                Assert.NotEmpty(innerResult.Lists);
            }
        }
        
        [Theory]
        [Trait("Category", "MongoApi")]
        [InlineData("Gsdfkjsdfijksjfe", 404, "The user you queried does not exist")]
        [InlineData(" ", 400, "min length is 3")]
        public void UserShouldReturnErrorCodes(string user, int errorcode, string errormessage)
        {

            var request = new RequestString
            {
                user = user
            };

            var requestString = CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
            var innerResult = _fixture.MongoApi.GetUser(requestString) as ErrorModel;
        
            Assert.Equal(errorcode, innerResult.statusCode);
            Assert.Contains(errormessage, innerResult.message);
        }
        
    }
}