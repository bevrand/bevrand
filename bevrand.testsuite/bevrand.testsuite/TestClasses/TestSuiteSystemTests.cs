using System;
using System.Net.Http.Headers;
using System.Threading;
using bevrand.testsuite.Models.AuthenticationApi;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Remote;
using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestSuiteSystemTests
    {
        private readonly TestSuiteFixture _fixture;  
        
        public TestSuiteSystemTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }

        [Fact]
        [Trait("Category", "SystemTest")]
        public void CreateAUserAndAuthenticateThatTheUserExistsAndHasAValidPassword()
        {
            var userToCreate = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            
            using (var driver = new RemoteWebDriver(new Uri(_fixture.SeleniumHubUrl), _fixture.DriverCapabilities))
            //using(var driver = new ChromeDriver())
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                //driver.Navigate().GoToUrl("http://0.0.0.0:4540/");
                driver.FindElementByXPath(@"//*[@id=""navbarResponsive""]/ul/li[2]/a").Click();
                Thread.Sleep(1500);

                var userName = driver.FindElementById("userName");
                userName.SendKeys(userToCreate.userName);
                var email = driver.FindElementById("emailAddress");
                email.SendKeys(userToCreate.emailAddress);
                var password = driver.FindElementById("passWord");
                var retypedPassword = driver.FindElementById("controlPassWord");
                password.SendKeys(userToCreate.passWord);
                retypedPassword.SendKeys(userToCreate.passWord);
                driver.FindElementByXPath(@"//*[@id=""root""]/div/div/span/div/form/button").Click();
                Thread.Sleep(1000);
                var registerSuccessful =
                    driver.FindElementByXPath(@"//*[@id=""root""]/div/div/span/div/form/button").Text.ToUpperInvariant()
                        .Replace(" ", "");
                Assert.Equal("LOGIN", registerSuccessful);
            }
            
            var requeststring = _fixture.AuthenticationUrl + $"/api/Users/";
            var response = _fixture.BaseApiClient.GenericGet<ListUserResponse>(requeststring).Result as ListUserResponse;

            Assert.Equal(200, response.StatusCode);
            foreach (var user in response.AllUsers)
            {
                if (user.username == userToCreate.userName.ToLowerInvariant())
                {
                    Assert.Equal(user.emailAddress, userToCreate.emailAddress);
                    requeststring = _fixture.AuthenticationUrl + "/api/Validate";
                    var requestValidate = new ValidateUser
                    {
                        userName = userToCreate.userName.ToLowerInvariant(),
                        passWord = userToCreate.passWord
                    };

                    var resp = _fixture.AuthenicationApi.PostAValidation(requeststring, requestValidate).Result as ValidatePostResult;
            
                    Assert.Equal(200, resp.StatusCode);
                    Assert.True(resp.Valid);
                }
            }
        }
        
        
        [Fact]
        [Trait("Category", "SystemTest")]
        public void CreateAUserAndAuthenticateThatTheUserCanLogInAndCreateAList()
        {
            var userToCreate = new PostModelAuthentication
            {
                userName = Helpers.RandomNameGenerator.RandomString(25).ToLowerInvariant(),
                emailAddress = Helpers.RandomNameGenerator.RandomEmail(),
                active = true,
                passWord = "thisisatestpassword"
            };
            
            
            using (var driver = new RemoteWebDriver(new Uri(_fixture.SeleniumHubUrl), _fixture.DriverCapabilities))
           // using(var driver = new ChromeDriver())
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
               // driver.Navigate().GoToUrl("http://0.0.0.0:4540/");
                driver.FindElementByXPath(@"//*[@id=""navbarResponsive""]/ul/li[2]/a").Click();
                Thread.Sleep(1500);

                var userName = driver.FindElementById("userName");
                userName.SendKeys(userToCreate.userName);
                var email = driver.FindElementById("emailAddress");
                email.SendKeys(userToCreate.emailAddress);
                var password = driver.FindElementById("passWord");
                var retypedPassword = driver.FindElementById("controlPassWord");
                password.SendKeys(userToCreate.passWord);
                retypedPassword.SendKeys(userToCreate.passWord);
                driver.FindElementByXPath(@"//*[@id=""root""]/div/div/span/div/form/button").Click();
                Thread.Sleep(1000);
                

                userName = driver.FindElementById("userName");
                userName.SendKeys(userToCreate.userName);
                email = driver.FindElementById("emailAddress");
                email.SendKeys(userToCreate.emailAddress);
                password = driver.FindElementById("passWord");
                password.SendKeys(userToCreate.passWord);
                driver.FindElementByXPath(@"//*[@id=""root""]/div/div/span/div/form/button").Click();
                Thread.Sleep(1000);
                
                driver.FindElementByXPath(@"//*[@id=""navbarResponsive""]/ul/li[4]/a").Click();
                var topTextCreate = driver.FindElementById("currentlySelectedPlaylist").Text;
                Assert.Contains(userToCreate.userName, topTextCreate);

                var displayName = driver.FindElementById("displayName");
                displayName.SendKeys("SELENIUMDOESATEST");
                var beverages = driver.FindElementById("beverages");
                beverages.SendKeys("Wine, Beer, Whiskey, Campari");
                driver.FindElementByXPath(@"//*[@id=""playlistCreator""]/div/div/div/form/button").Click();
                
            }
        }
    }
}


        
