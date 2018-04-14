using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using bevrand.testsuite.Helpers;
using bevrand.testsuite.Models.MongoApi;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Interactions;
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
            using (var driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var title = driver.Title;
                Assert.Equal("The Beverage Randomizer", title);
            }
        }
        
        [Theory]
        [Trait("Category", "FrontEnd")]
        [InlineData("letsGetStartedButton")]
        [InlineData("currentlySelectedPlaylist")]
        public void TopPageButtonsScrollDown(string button)
        {
            using (var driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var letsGetStarted =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id(button)));
                letsGetStarted.Click();
                var displayName = driver.FindElementById("currentlySelectedPlaylist").Text;
                Assert.NotNull(displayName);
            }
        }

        
        [Fact]
        [Trait("Category", "FrontEnd")]
        public void WhatWasRandomizedButtonScrollsDown()
        {
            using (RemoteWebDriver driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var chooseList =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id("topFiveLinkButton")));
                chooseList.Click();
                
                const string expectedText = "Thank God It's Friday!";
                var randomListText = driver.FindElementById("currentlySelectedPlaylist").Text;
                
                Assert.Equal(expectedText, randomListText);
            }
        }

        [Fact]
        [Trait("Category", "FrontEnd")]
        public void RandomizeButtonRandomizesADrink()
        {
            var beverages = new List<string>();
            const string expectedText = "you have randomized:";

            using (var driver =
                new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var chooseList =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id("letsGetStartedButton")));
                chooseList.Click();

                var listName = driver.FindElementByXPath(@"//*[@id=""getstarted""]/div/div[4]/div/div/ul");
                var drinks = listName.FindElements(By.TagName("li"));
                foreach (var drink in drinks)
                {
                    beverages.Add(drink.Text.ToLowerInvariant().Replace(" ", ""));
                }

                Thread.Sleep(500);
                var randomizeButton = driver.FindElementById("randomizeButton");
                randomizeButton.Click();

                var randomizedOutput =
                    wait.Until(ExpectedConditions.ElementIsVisible(By.XPath(@"//*[@id=""randomizedOutput""]/div")));
                var randomizedDrink = randomizedOutput.Text.ToLowerInvariant();
                var specificDrink = randomizedDrink.Substring(randomizedDrink.LastIndexOf(':') + 1).Replace(" ", "");

                Console.WriteLine(randomizedDrink);
                Assert.Contains(expectedText, randomizedDrink);
                Console.WriteLine(specificDrink);
                Assert.Contains(specificDrink, beverages);
            }
        }
        
        [Fact]
        [Trait("Category", "FrontEnd")]
        public void RandomizeButtonShouldIncreaseTheTopFive()
        {
            
            var beverages = new List<string>();
            var rolledBeverages = new List<string>();

            using (var driver =
                new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var chooseList =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id("letsGetStartedButton")));
                chooseList.Click();

                Thread.Sleep(1000);
                var randomizeButton = driver.FindElementById("randomizeButton");
                randomizeButton.Click();

                for (var i = 0; i < 5; i++)
                {
                    randomizeButton.Click();
                    var randomizedOutput =
                        wait.Until(ExpectedConditions.ElementIsVisible(By.XPath(@"//*[@id=""randomizedOutput""]/div")));
                    var randomizedDrink = randomizedOutput.Text.ToLowerInvariant().Split();
                    var specificDrink = randomizedDrink[3];
                    beverages.Add(specificDrink);
                }

                var action = new Actions(driver);
                action.SendKeys(Keys.PageDown).Build().Perform();

                var listName = driver.FindElementByXPath(@"//*[@id=""redisHistoryForList""]/div/ul");
                var rolled = listName.FindElements(By.TagName("li"));
                foreach (var drink in rolled)
                {
                    var splittedWords = drink.Text.ToLowerInvariant().Split();
                    var drinkToAdd = splittedWords[0];
                    rolledBeverages.Add(drinkToAdd);
                }

                foreach (var rolledDrink in beverages)
                {
                    Assert.Contains(rolledDrink, rolledBeverages);
                }
            }
        }
        
        
        [Fact]
        [Trait("Category", "FrontEnd")]
        public void SwitchFromTopFiveToAllShouldIncreaseLengthOfArray()
        {

            using (var driver =
                new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var chooseList =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id("letsGetStartedButton")));
                chooseList.Click();

                var listName = driver.FindElementByXPath(@"//*[@id=""getstarted""]/div/div[4]/div/div/ul");
                var drinks = listName.FindElements(By.TagName("li"));
                if (drinks.Count > 5)
                {
                    Thread.Sleep(1000);
                    var randomizeButton = driver.FindElementById("randomizeButton");
                    randomizeButton.Click();

                    for (var i = 0; i < 40; i++)
                    {
                        randomizeButton.Click();
                        Thread.Sleep(200);
                    }

                    var action = new Actions(driver);
                    action.SendKeys(Keys.PageDown).Build().Perform();
                    
                    Thread.Sleep(1000);

                    
                    var randomButton = driver.FindElementById("topFiveSwitchButton").Text.ToLowerInvariant();
                    if (randomButton.Contains("all drinks"))
                    {
                        driver.FindElementById("topFiveSwitchButton").Click();
                        driver.FindElementById("topFiveSwitchButton").Click();
                        var rolledDrinks = driver.FindElementByXPath(@"//*[@id=""redisHistoryForList""]/div/ul");
                        var rolledAll = rolledDrinks.FindElements(By.TagName("li"));
                        Assert.True(rolledAll.Count <= drinks.Count); 

                        driver.FindElementById("topFiveSwitchButton").Click();

                        randomButton = driver.FindElementById("topFiveSwitchButton").Text.ToLowerInvariant();
                        Assert.Contains("top five", randomButton);
                        rolledDrinks = driver.FindElementByXPath(@"//*[@id=""redisHistoryForList""]/div/ul");
                        var rolledTopFive = rolledDrinks.FindElements(By.TagName("li"));
                        Console.WriteLine($"Rolled all: {rolledAll.Count} Rolled top five {rolledTopFive.Count}");
                        Assert.True(rolledAll.Count >= rolledTopFive.Count);
                    }

                }
            }
        }

        [Fact]
        [Trait("Category", "FrontEnd")]
        public void SwitchFromTopFiveButtonIsClickable()
        {
            using (var driver =
                new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                //driver.Navigate().GoToUrl("http://0.0.0.0:4540/");
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));

                Thread.Sleep(1000);
                
                var action = new Actions(driver);
                action.SendKeys(Keys.PageDown).Build().Perform();
                

                driver.FindElementById("topFiveSwitchButton").Click();

                var randomButton = driver.FindElementById("topFiveSwitchButton").Text.ToLowerInvariant();
                if (randomButton.Contains("all drinks"))
                {
                    Assert.Contains("all drinks", randomButton);
                    driver.FindElementById("topFiveSwitchButton").Click();
                    randomButton = driver.FindElementById("topFiveSwitchButton").Text.ToLowerInvariant();
                    Assert.Contains("top five", randomButton);
                }
                else if (randomButton.Contains("top five"))
                {
                    Assert.Contains("top five", randomButton);
                    driver.FindElementById("topFiveSwitchButton").Click();
                    randomButton = driver.FindElementById("topFiveSwitchButton").Text.ToLowerInvariant();
                    Assert.Contains("all drinks", randomButton);
                }
            }
        }

        [Fact]
        [Trait("Category", "FrontEnd")]
        public void GetAListFromMongoApiAndAssertAllDrinksArePresentStandardList()
        {            
            var response = _fixture.MongoApi.FrontPageGetWithoutList() as FrontPageListResponse;

            Assert.Equal(200, response.StatusCode);

            var beverages = new List<string>();
            string displayName;

            using (var driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
              
                var letsGetStarted =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id("letsGetStartedButton")));
                letsGetStarted.Click();
                
                displayName = driver.FindElementById("currentlySelectedPlaylist").Text;
                var listName = driver.FindElementByXPath(@"//*[@id=""getstarted""]/div/div[4]/div/div/ul");
                var drinks = listName.FindElements(By.TagName("li"));
                foreach (var drink in drinks)
                {
                    beverages.Add(drink.Text.ToLowerInvariant());
                }
            }
            
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

            Assert.Equal(200, response.StatusCode);

            var beverages = new List<string>();
            string displayName;

            using (var driver = new RemoteWebDriver(new Uri("http://0.0.0.0:4444/wd/hub"), _fixture.DriverCapabilities))
       //     using(var driver = new ChromeDriver())
            {
                driver.Navigate().GoToUrl("http://nodefrontend:5000");
                //driver.Navigate().GoToUrl("http://0.0.0.0:4540/");
                var wait = new WebDriverWait(driver, TimeSpan.FromMilliseconds(5000));
                var letsGetStarted =
                    wait.Until(ExpectedConditions.ElementToBeClickable(By.Id("letsGetStartedButton")));
                letsGetStarted.Click();


              //  driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromMilliseconds(100);
                Thread.Sleep(1000);
                var chooseList =
                    wait.Until(ExpectedConditions.ElementToBeClickable(
                        By.Id("chooseListBottomButton")));
                
                chooseList.Click();
                
                var portFolioElement = driver.FindElementByXPath(@"//*[@id=""playlists""]/div/div/div[5]/a/div/div");
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