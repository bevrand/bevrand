using System;
using System.Diagnostics.Tracing;
using System.Linq;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.AuthenticationApi;
using Microsoft.VisualStudio.TestPlatform.CommunicationUtilities;
using Newtonsoft.Json.Linq;
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

        [Fact]
        [Trait("Category", "Authentication")]
        public void GetUserByIdReturnsSuccess()
        {
            var poststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var resp = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(poststring, request).Result as PostModelResponse;
            
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/{resp.id}";
            var response = _fixture.BaseApiClient.GenericGet<UserResponse>(requeststring).Result;

            Assert.Equal(200, response.StatusCode);
        }  
        
        [Theory]
        [Trait("Category", "Authentication")]
        [InlineData(Int16.MaxValue, "was not found")]
        [InlineData(Int16.MinValue, "was not found")]
        public void GetUserByIdThatDoesNotExistGivesAnError(int id, string message)
        {
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/{id}/";
            var response = _fixture.BaseApiClient.GenericGet<UserResponse>(requeststring).Result as BaseErrorResponse;

            Assert.Equal(404, response.StatusCode);
            Assert.Contains(message, response.UserError);
        }   
        
        [Fact]
        [Trait("Category", "Authentication")]
        public void GetUserByEmailReturnsSuccess()
        {
            var poststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var resp = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(poststring, request).Result as PostModelResponse;
            
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/by-email/{resp.emailAddress}";
            var response = _fixture.BaseApiClient.GenericGet<UserResponse>(requeststring).Result as UserResponse;

            Assert.Equal(200, response.StatusCode);
            Assert.Equal(resp.emailAddress, response.emailAddress);
            Assert.Equal(resp.id, response.id);
        }  
        

        
        [Fact]
        [Trait("Category", "Authentication")]
        public void GetUserByUserNameReturnsSuccess()
        {
            var poststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var resp = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(poststring, request).Result as PostModelResponse;
            
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/{resp.id}";
            var response = _fixture.BaseApiClient.GenericGet<UserResponse>(requeststring).Result as UserResponse;

            Assert.Equal(200, response.StatusCode);
            Assert.Equal(resp.userName, response.username);
            Assert.Equal(resp.id, response.id);
        }  
        
        [Theory]
        [Trait("Category", "Authentication")]
        [InlineData("thisuserdoesnotexistandifitdoessomeonemadeamistake", "was not found")]
        public void GetUserByUsernameThatDoesNotExistGivesAnError(string username, string message)
        {
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/{username}/";
            var response = _fixture.BaseApiClient.GenericGet<UserResponse>(requeststring).Result as BaseErrorResponse;

            Assert.Equal(404, response.StatusCode);
            Assert.Contains(message, response.UserError);
        } 
        
        [Fact]
        [Trait("Category", "Authentication")]
        public void GetListOfUsersReturnsSucces()
        {            
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/";
            var response = _fixture.BaseApiClient.GenericGet<ListUserResponse>(requeststring).Result as ListUserResponse;

            Assert.Equal(200, response.StatusCode);
            var tempId = int.MaxValue;
            foreach (var user in response.AllUsers)
            {
                Assert.NotNull(user.id);
                Assert.NotEqual(tempId, user.id);
                tempId = user.id;
            }
        }

        [Fact]
        [Trait("Category", "Authentication")]
        public void PostAUserReturnsASuccesCode()
        {
            var requeststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var response = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(requeststring, request).Result as PostModelResponse;

            Assert.Equal(201, response.StatusCode);
            Assert.Equal(request.userName.ToLowerInvariant(), response.userName);
            Assert.Equal(request.emailAddress, response.emailAddress);
        }
        
        [Fact]
        [Trait("Category", "Authentication")]
        public void PostAUserTwiceWillResultInAnError()
        {
            var requeststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var response = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(requeststring, request).Result;

            Assert.Equal(201, response.StatusCode);
            
            response = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(requeststring, request).Result;
            Assert.Equal(400, response.StatusCode);
        }

        [Theory]
        [Trait("Category", "Authentication")]
        [InlineData(null, null, null, "You have to provide a user")]
        [InlineData(null, "test@test.nl", "password", "You have to provide a user")]
        [InlineData("SomeRandomUserForPost", "test@test.nl", null, "You have to provide a valid password")]
        [InlineData("SomeRandomUserForPost", "testtest", "password", "was not a valid mailaddress")]
        public void FaultyPostsDoNotGetEnteredIntoTheDatabse(string username, string email, string password, string message)
        {
            var requeststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new PostModelAuthentication
            {
                userName = username,
                emailAddress = email,
                active = true,
                passWord = password
            };
            var response = _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(requeststring, request).Result as BaseErrorResponse;

            Assert.Equal(400, response.StatusCode);
            Assert.Contains(message, response.UserError);

        }
        
        
        [Fact] 
        [Trait("Category", "Authentication")]
        public void DeleteAUserOnceShouldReturnsSuccesCode()
        {
            var requeststring = _fixture.AuthenticationUrl + "/api/Users/";
            var requestPost = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var response =
                _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(requeststring, requestPost).Result as
                    PostModelResponse;
            
            var request = new IdBasedQueryModel
            {
                Id = response.id
            };

            var queryString =
                Helpers.CreateApiRequestString.GetQueryStringFromModel<IIdBasedQueryModel, IdBasedQueryModel>(request);
            var requestDelete = requeststring + queryString;
            var deletedResponse = _fixture.BaseApiClient.GenericDeleteObject(requestDelete);
            
            Assert.Equal(204, deletedResponse.StatusCode);

        }
        
        [Fact] 
        [Trait("Category", "Authentication")]
        public void DeletingAUserTwiceReturnsAnError()
        {
            var requeststring = _fixture.AuthenticationUrl + "/api/Users/";
            var requestPost = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            var response =
                _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(requeststring, requestPost).Result as
                    PostModelResponse;

            var request = new IdBasedQueryModel
            {
                Id = response.id
            };

            var queryString =
                Helpers.CreateApiRequestString.GetQueryStringFromModel<IIdBasedQueryModel, IdBasedQueryModel>(request);
            var requestDelete = requeststring + queryString;
            var deletedResponse = _fixture.BaseApiClient.GenericDeleteObject(requestDelete);
            
            Assert.Equal(204, deletedResponse.StatusCode);
            
            deletedResponse = _fixture.BaseApiClient.GenericDeleteObject(requestDelete);
            
            Assert.Equal(404, deletedResponse.StatusCode);            
        }
        
        [Fact] 
        [Trait("Category", "Authentication")]
        public void CannotDeleteUserThatDoesNotExist()
        {
            var requeststring = _fixture.AuthenticationUrl + "/api/Users/";
            var request = new IdBasedQueryModel
            {
                Id = int.MaxValue
            };

            var queryString =
                Helpers.CreateApiRequestString.GetQueryStringFromModel<IIdBasedQueryModel, IdBasedQueryModel>(request);
            var requestDelete = requeststring + queryString;
            var deletedResponse = _fixture.BaseApiClient.GenericDeleteObject(requestDelete);
            
            Assert.Equal(404, deletedResponse.StatusCode);

        }
        
        [Theory]
        [Trait("Category", "Authentication")]
        [InlineData("notnull", "notnull")]
        [InlineData(null, "notnull")]
        [InlineData("notnull", null)]
        public void CanValidateByEmailAndUserNameWithValidPassWord(string username, string email)
        {
            var postString = _fixture.AuthenticationUrl + "/api/Users/";
            var requestPost = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            
            var response =
                _fixture.BaseApiClient.GenericPostObject<PostModelResponse>(postString, requestPost).Result as
                    PostModelResponse;
            
            Assert.Equal(201, response.StatusCode);
            if (username != null)
            {
                username = requestPost.userName.ToLowerInvariant();
            }

            if (email != null)
            {
                email = requestPost.emailAddress;
            }
            var requeststring = _fixture.AuthenticationUrl + "/api/Validate/";
            var requestValidate = new ValidateUser
            {
                emailAddress = email,
                userName = username,
                passWord = requestPost.passWord
            };

            var resp = _fixture.AuthenicationApi.PostAValidation(requeststring, requestValidate).Result as ValidatePostResult;
            
            Assert.Equal(200, resp.StatusCode);
            Assert.True(resp.Valid);

        }
    }
}