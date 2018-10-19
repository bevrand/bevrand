using System;
using System.Collections.Generic;
using bevrand.testsuite.Helpers;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.PlaylistApi;
using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestSuitePlayListApiTests
    {
        private readonly TestSuiteFixture _fixture;
        
        public TestSuitePlayListApiTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }

        /// <summary>
        /// Tests the public list tgif that should always be present
        /// </summary>
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldBeAbleToRetrieveAStandardPublicPlaylist()
        {
            var requestUrl = _fixture.PlayListUrl + "/public/tgif";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageResponse>(requestUrl).Result as PublicPageResponse;
            
            Assert.Equal(200, response.StatusCode);
            Assert.NotEmpty(response.result.beverages);
        }
        
        /// <summary>
        /// Tests that public lists should be returned
        /// </summary>
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldBeAbleToRetrieveAllPublicPlaylists()
        {
            var requestUrl = _fixture.PlayListUrl + "/public";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageListResponse>(requestUrl).Result as PublicPageListResponse;
            
            Assert.Equal(200, response.StatusCode);
        }

        /// <summary>
        /// All lists returned should give a 200 and have data
        /// </summary>
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldBeAbleToGetMoreDetailsOnEachReturnedPlaylist()
        {
            var requestUrl = _fixture.PlayListUrl + "/public";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageListResponse>(requestUrl).Result as PublicPageListResponse;
            
            Assert.Equal(200, response.StatusCode);

            foreach (var resp in response.result)
            {
                var requestString = $"{requestUrl}/{resp.list}";
                var innerResult = _fixture.BaseApiClient.FlurlGet<PublicPageResponse>(requestString).Result as PublicPageResponse;
            
                Assert.Equal(200, innerResult.StatusCode);
                Assert.Equal(resp.list, innerResult.result.list);
                Assert.NotEmpty(innerResult.result.beverages);
            }
        }
        
        /// <summary>
        /// Test with a random guid that should throw a 404
        /// </summary>
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        [InlineData("Gsdfkjsdfijksjfe", 404, "List could not be found")]
        [InlineData("%20", 400, "min length is 2")]
        [InlineData("o", 400, "min length is 2")]
        public void PublicListThatDoesNotExistsReturnsAnError(string list, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/public/{list}";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageResponse>(requestUrl).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }


        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        public void ShouldBeAbleToCreateANewPlaylistAndUserCombination()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);

            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, result.StatusCode);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        public void ListNamesShouldAllBeLowerCase()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, result.StatusCode);

            requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}";
            var response = _fixture.BaseApiClient.FlurlGet<PrivatePageUserPlaylistsResponse>(requestUrl).Result as PrivatePageUserPlaylistsResponse;
            
            Assert.Equal(200, response.StatusCode);
            Assert.NotEmpty(response.result);
            foreach (var ch in response.result[0])
            {
                if (Char.IsLetter(ch))
                {
                    Assert.True(Char.IsLower(ch));
                }
            }
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        public void ShouldBeAbleToCreateNewListForExistingUser()
        {
            var username = "marvin";
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, result.StatusCode);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        [InlineData("%20", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 2")]
        [InlineData("o", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 2")]
        [InlineData("listname", "d", "http://www.testimage.com/image.png", "beer", 400, "min length is 3")]
        [InlineData("listname", " ", "http://www.testimage.com/image.png", "beer", 400, "min length is 3")]
        [InlineData("listname", "displayname", "i", "beer", 400, "min length is 3")]
        [InlineData("listname", "displayname", " ", "beer", 400, "min length is 3")]
        [InlineData("listname", "displayname", "http://www.testimage.com/image.png", "b", 400, "min length is 2")]
        [InlineData("listname", "displayname", "http://www.testimage.com/image.png", " ", 400, "min length is 2")]
        public void ShouldNotBeAbleToPostInvalidData(string list, string displayName, string imageUrl, string beverage, int errorcode, string errormessage)
        {
            var username = RandomNameGenerator.RandomString(25);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{list}";

            var playList = new BasePlaylist
            {
                displayName = displayName,
                imageUrl = imageUrl,
                beverages = new List<string>
                {
                    beverage,
                    beverage
                }
            };

            var response = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseErrorResponse>(requestUrl, playList).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        [InlineData("listname", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 2")]
        public void ShouldNotBeAbleToPostAPlaylistWithOnlyOneDrink(string list, string displayName, string imageUrl, string beverage, int errorcode, string errormessage)
        {
            var username = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{playListName}";

            var playList = new CreatePlayList
            {
                list = list,
                displayName = displayName,
                imageUrl = imageUrl,
                beverages = new List<string>
                {
                    beverage
                }
            };

            var response = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseErrorResponse>(requestUrl, playList).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        public void ShouldNotBeAbleToCreateTheSamePlayListForSameUserTwice()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, result.StatusCode);
            
            var res = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result as BaseErrorResponse;
            
            Assert.Equal(400, res.StatusCode);
            Assert.Contains("User and list combination already exists", res.UserError);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        public void ShouldBeAbleToCreateSamePlayListForDifferentUser()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, result.StatusCode);
            
            newUserName = RandomNameGenerator.RandomString(25);
            requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";
            var res = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, res.StatusCode);
        }

        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        [InlineData("%20", 400, "min length is 3")]
        [InlineData("o", 400, "min length is 3")]
        public void ShouldNotBeAbleToPostToAnInvalidUserName(string list, int errorcode, string errormessage)
        {
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{list}/{playListName}";
            var playList = this.MapNewPlaylist();
            var response = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Post")]
        public void ShouldNotBeAbleToPostAFrontPageList()
        {
            var username = "frontpage";
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            Assert.Equal(403, result.StatusCode);
        }

        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldBeAbleToRetrieveAStandardPrivatePlaylist()
        {
            var username = "marvin";
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}";

            var response = _fixture.BaseApiClient.FlurlGet<PrivatePageUserPlaylistsResponse>(requestUrl).Result as PrivatePageUserPlaylistsResponse;
            
            Assert.Equal(200, response.StatusCode);
            Assert.NotEmpty(response.result);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        [InlineData("%20", 400, "min length is 3")]
        [InlineData("o", 400, "min length is 3")]
        public void ShouldNotBeAbleToFindInvalidUsers(string username, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}";

            var response = _fixture.BaseApiClient.FlurlGet<PrivatePageUserPlaylistsResponse>(requestUrl).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldGetA200ReponseWhenListDoesNotExist()
        {
            var username = Guid.NewGuid();
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}";

            var response = _fixture.BaseApiClient.FlurlGet<PrivatePageUserPlaylistsResponse>(requestUrl).Result as PrivatePageUserPlaylistsResponse;
            
            Assert.Equal(200, response.StatusCode);
            Assert.Empty(response.result);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldBeAbleToRetrieveAStandardPrivatePlaylistWithList()
        {
            var username = "marvin";
            var listname = "paranoid";
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{listname}";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageResponse>(requestUrl).Result as PublicPageResponse;
            
            Assert.Equal(200, response.StatusCode);
            Assert.NotEmpty(response.result.beverages);
            Assert.Equal(username, response.result.user);
            Assert.Equal(listname, response.result.list);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        public void ShouldBeAbleToRetrieveAPlayListThatWasJustCreated()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            
            Assert.Equal(201, result.StatusCode);
            
            requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageResponse>(requestUrl).Result as PublicPageResponse;
            
            Assert.Equal(200, response.StatusCode);
            Assert.NotEmpty(response.result.beverages);
            Assert.Equal(newUserName.ToLower(), response.result.user);
            Assert.Equal(playListName.ToLower(), response.result.list);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        [InlineData("%20", "sdf", 400, "min length is 3")]
        [InlineData("o", "sdfs", 400, "min length is 3")]
        [InlineData("asdasf", "o", 400, "min length is 2")]
        [InlineData("oqwa", "%20", 400, "min length is 2")]
        [InlineData("ssdfsef3fssf", "ssdfsef3fssf", 404, "List could not be found")]
        [InlineData("marvin", "ssdfsef3fssf", 404, "List could not be found")]
        [InlineData("ssdfsef3fssf", "paranoid", 404, "List could not be found")]
        public void ShouldNotBeAbleToFindInvalidPlayLists(string username, string listname, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{listname}";

            var response = _fixture.BaseApiClient.FlurlGet<PublicPageResponse>(requestUrl).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Delete")]
        public void ShouldBeAbleToDeleteACreatedPlayList()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            Assert.Equal(201, result.StatusCode);
            
            requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";
            var response = _fixture.BaseApiClient.FlurlDelete(requestUrl);
            Assert.Equal(204, response.StatusCode);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Delete")]
        public void ShouldBeAbleToDeleteACreatedUser()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            Assert.Equal(201, result.StatusCode);
            
            requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}";
            var response = _fixture.BaseApiClient.FlurlDelete(requestUrl);
            Assert.Equal(204, response.StatusCode);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Delete")]
        [InlineData("%20", 400, "min length is 3")]
        [InlineData("o", 400, "min length is 3")]
        public void ShouldNotBeAbleToDeleteInvalidUsers(string username, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}";

            var response = _fixture.BaseApiClient.FlurlDelete(requestUrl) as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Delete")]
        [InlineData("%20", 400, "min length is 2")]
        [InlineData("o", 400, "min length is 2")]
        public void ShouldNotBeAbleToDeleteInvalidPlaylist(string listname, int errorcode, string errormessage)
        {
            var username = "marvin";
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{listname}";

            var response = _fixture.BaseApiClient.FlurlDelete(requestUrl) as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Delete")]
        [InlineData("iamnotauser", "somerandomlist", 404, "User could not be found")]
        [InlineData("marvin", "somerandomlist", 404, "List could not be found")]
        [InlineData("iamnotauser", null, 404, "User could not be found")]
        public void NonExistentUsersAndListsReturnA404(string username, string listname, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{listname}";
            if (listname is null)
            {
                requestUrl = $"{_fixture.PlayListUrl}/private/{username}";
            }

            var response = _fixture.BaseApiClient.FlurlDelete(requestUrl) as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }

        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Put")]
        public void ShouldBeAbleToUpdateACreatedUser()
        {
            var newUserName = RandomNameGenerator.RandomString(25);
            var playListName = RandomNameGenerator.RandomString(10);
            var requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName}/{playListName}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlPostCreatedWithoutAResponse<BaseResponseModel>(requestUrl, playList).Result;
            Assert.Equal(201, result.StatusCode);

            var updatedPlaylist = this.MapUpdatedList();
            
            requestUrl = $"{_fixture.PlayListUrl}/private/{newUserName.ToLower()}/{playListName}";
            var response = _fixture.BaseApiClient.FlurlUpdate<BaseResponseModel>(requestUrl, updatedPlaylist).Result;
            Assert.Equal(204, response.StatusCode);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Update")]
        [InlineData("iamnotauser", "whatever", 404, "List could not be found")]
        [InlineData("marvin", "somerandomlistthatisnotthere", 404, "List could not be found")]
        public void ShouldNotBeAbleToUpdateNonExistentUsersOrLists(string username, string listname, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{listname}";
            
            var updatedPlaylist = this.MapUpdatedList();
            var response = _fixture.BaseApiClient.FlurlUpdate<BaseErrorResponse>(requestUrl, updatedPlaylist).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Theory]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Get")]
        [InlineData("%20", "listname", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 3")]
        [InlineData("o", "listname", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 3")]
        [InlineData("username", "%20", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 2")]
        [InlineData("username", "o", "displayname", "http://www.testimage.com/image.png", "beer", 400, "min length is 2")]
        [InlineData("username","listname", "d", "http://www.testimage.com/image.png", "beer", 400, "min length is 3")]
        [InlineData("username","listname", " ", "http://www.testimage.com/image.png", "beer", 400, "min length is 3")]
        [InlineData("username","listname", "displayname", "i", "beer", 400, "min length is 3")]
        [InlineData("username","listname", "displayname", " ", "beer", 400, "min length is 3")]
        [InlineData("username","listname", "displayname", "http://www.testimage.com/image.png", "b", 400, "min length is 2")]
        [InlineData("username","listname", "displayname", "http://www.testimage.com/image.png", " ", 400, "min length is 2")]
        public void ShouldNotBeAbleToUpdateInvalidData(string username, string list, string displayName, string imageUrl, string beverage, int errorcode, string errormessage)
        {
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{list}";

            var playList = new BasePlaylist
            {
                displayName = displayName,
                imageUrl = imageUrl,
                beverages = new List<string>
                {
                    beverage,
                    beverage
                }
            };

            var response = _fixture.BaseApiClient.FlurlUpdate<BaseErrorResponse>(requestUrl, playList).Result as BaseErrorResponse;
            
            Assert.Equal(errorcode, response.StatusCode);
            Assert.Contains(errormessage, response.UserError);
        }
        
        [Fact]
        [Trait("Category", "PlaylistApi")]
        [Trait("Category", "Put")]
        public void ShouldNotBeAbleToUpdateAFrontPageList()
        {
            var username = "frontpage";
            var listname = "tgif";
            var requestUrl = $"{_fixture.PlayListUrl}/private/{username}/{listname}";

            var playList = this.MapNewPlaylist();

            var result = _fixture.BaseApiClient.FlurlUpdate<BaseResponseModel>(requestUrl, playList).Result;
            Assert.Equal(404, result.StatusCode);
        }
        
        private BasePlaylist MapNewPlaylist()
        {
            return new BasePlaylist
            {
                displayName = RandomNameGenerator.RandomString(15),
                imageUrl = "http://www.testimage.com/image.png",
                beverages = new List<string>
                {
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5)
                }
            };
        }
        
        private BasePlaylist MapUpdatedList()
        {
            return new BasePlaylist
            {
                displayName = RandomNameGenerator.RandomString(15),
                imageUrl = "http://www.testimage.com/image.png",
                beverages = new List<string>
                {
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5),
                    RandomNameGenerator.RandomString(5)
                }
            };
        }
    }
}