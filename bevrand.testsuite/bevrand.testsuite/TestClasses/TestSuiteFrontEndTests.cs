using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Threading;
using bevrand.testsuite.Helpers;
using bevrand.testsuite.Models.MongoApi;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Remote;
using OpenQA.Selenium.Support.UI;
using Xunit;

namespace bevrand.testsuite.TestClasses
{
    [Collection("TestSuite Collection")]
    public class TestSuiteFrontEndTests
    {
        private readonly TestSuiteFixture _fixture;
        
        public TestSuiteFrontEndTests(TestSuiteFixture _fixture)
        {
            this._fixture = _fixture;
        }

        [Fact]
        [Trait("Category", "FrontEnd")]
        public void SeeIfTitleOfPageIsCorrect()
        {
            using (RemoteWebDriver driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var title = driver.Title;
                Assert.Equal("The Beverage Randomizer", title);
            }
        }
        
        [Fact]
        [Trait("Category", "FrontEnd")]
        public void LetsGetStartedButtonShouldScrollDown()
        {
            using (RemoteWebDriver driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var element =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.XPath(@"//*[@id=""page-top""]/header/div/div/a[1]")));
                element.Click();
                Thread.Sleep(1000);
                var displayName = driver.FindElementById("currentlySelectedPlaylist").Text;
                Console.WriteLine(displayName);
                Assert.NotNull(displayName);
            }
        }
        
         [Fact]
        [Trait("Category", "FrontEnd")]
        public void GetAListFromMongoApiAndAssertAllDrinksArePresentStandardList()
        {            
            var response = _fixture.MongoApi.FrontPageGetWithoutList() as FrontPageListResponse;

            Assert.Equal(200, response.statusCode);

            var beverages = new List<string>();
            string displayName;

            using (RemoteWebDriver driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
              
                var letsGetStarted =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.XPath(@"//*[@id=""page-top""]/header/div/div/a[1]")));
                letsGetStarted.Click();
                
                Thread.Sleep(500);
                displayName = driver.FindElementById("currentlySelectedPlaylist").Text;
                var listName = driver.FindElementByXPath(@"//*[@id=""getstarted""]/div/div[4]/div/div/ul");
                var drinks = listName.FindElements(By.TagName("li"));
                foreach (var drink in drinks)
                {
                    beverages.Add(drink.Text.ToLowerInvariant());
                }
            }
            
            Console.WriteLine(displayName);
            var selectedList = response.listOfFrontPages.First(n => n.displayName == displayName).list;

            var request = new RequestString
            {
                list = selectedList
            };
            var requestString =
                CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
            var selectedFrontPageUser = _fixture.MongoApi.FrontPageGetWithList(requestString) as FrontpageResponse;
            foreach (var drink in selectedFrontPageUser.beverages)
            {
                Assert.Contains(drink.ToLowerInvariant(), beverages);
            }
        }
        
        [Fact]
        [Trait("Category", "FrontEnd")]
        public void GetAListFromMongoApiAndAssertAllDrinksArePresentAnotherList()
        {            
            var response = _fixture.MongoApi.FrontPageGetWithoutList() as FrontPageListResponse;

            Assert.Equal(200, response.statusCode);

            var beverages = new List<string>();
            string displayName;

         //   using (RemoteWebDriver driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            using(var driver = new ChromeDriver())
            {
               // driver.Navigate().GoToUrl("http://nodefrontend:5000");
                driver.Navigate().GoToUrl("http://0.0.0.0:4540");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var letsGetStarted =
                    wait.Until(ExpectedConditions.ElementExists(By.XPath(@"//*[@id=""page-top""]/header/div/div/a[1]")));
                letsGetStarted.Click();


                //driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromMilliseconds(5000);
                var chooseList =
                    wait.Until(ExpectedConditions.ElementToBeClickable(
                        By.XPath(@"//*[@id=""getstarted""]/div/div[2]/div/a[2]")));
                
                #getstarted > div > div:nth-child(2) > div > a.btn.btn-primary.btn-xl.js-scroll-trigger
                
                chooseList.Click();


               // driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromMilliseconds(10000);
                var portFolioElement =
                    wait.Until(ExpectedConditions.ElementToBeClickable(
                        By.XPath(@"//*[@id=""portfolio""]/div/div/div[5]/a/div/div")));
                portFolioElement.Click();
                
                displayName = driver.FindElementById("currentlySelectedPlaylist").Text;
                var listName = driver.FindElementByXPath(@"//*[@id=""getstarted""]/div/div[4]/div/div/ul");
                var drinks = listName.FindElements(By.TagName("li"));
                foreach (var drink in drinks)
                {
                    beverages.Add(drink.Text.ToLowerInvariant());
                }
            }

            Console.WriteLine(displayName);
            var selectedList = response.listOfFrontPages.First(n => n.displayName == displayName).list;

            var request = new RequestString
            {
                list = selectedList
            };
            var requestString =
                CreateApiRequestString.GetQueryStringFromModel<IRequestString, RequestString>(request);
            var selectedFrontPageUser = _fixture.MongoApi.FrontPageGetWithList(requestString) as FrontpageResponse;
            foreach (var drink in selectedFrontPageUser.beverages)
            {
                Assert.Contains(drink.ToLowerInvariant(), beverages);
            }
        }
        
    }
    
}