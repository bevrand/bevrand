package com.beveragerandomizer.uittests;


import io.github.bonigarcia.SeleniumExtension;
import org.junit.Assert;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.By;
import org.openqa.selenium.Capabilities;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.phantomjs.PhantomJSDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SeleniumExtension.class)
public class FrontPageTests {

    Capabilities chromeCapabilities = DesiredCapabilities.chrome();
    Capabilities firefoxCapabilities = DesiredCapabilities.firefox();

    
    @Test
    public void pageComesUpAndHasCorrectTitle() throws MalformedURLException {
        // run against chrome
        RemoteWebDriver chrome = new RemoteWebDriver(new URL("http://0.0.0.0:4444/wd/hub"), chromeCapabilities);
        RemoteWebDriver firefox = new RemoteWebDriver(new URL("http://0.0.0.0:4444/wd/hub"), firefoxCapabilities);

        List<RemoteWebDriver> drivers = new ArrayList<>();
        drivers.add(chrome);
        drivers.add(firefox);

        for (RemoteWebDriver driver : drivers) {
            driver.get("http://nodefrontend:5000");
            assertTrue(driver.getTitle().startsWith("The Beverage Randomizer"));
            driver.quit();
        }
    }


    @Test
    public void thenScrollButtonWorks() throws MalformedURLException, InterruptedException {
        RemoteWebDriver chrome = new RemoteWebDriver(new URL("http://0.0.0.0:4444/wd/hub"), chromeCapabilities);
        RemoteWebDriver firefox = new RemoteWebDriver(new URL("http://0.0.0.0:4444/wd/hub"), firefoxCapabilities);

        List<RemoteWebDriver> drivers = new ArrayList<>();
        drivers.add(chrome);
        drivers.add(firefox);

        // run this test for firefox and for chrome
        for (RemoteWebDriver driver : drivers) {
            driver.get("http://nodefrontend:5000");
            driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
            driver.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();
            TimeUnit.SECONDS.sleep(2);

            //look for the randomize button
            WebElement randomizeButton = driver.findElement(By.id("randomize-button"));
            WebDriverWait wait = new WebDriverWait(driver, 10);
            wait.until(ExpectedConditions.elementToBeClickable(randomizeButton));
            randomizeButton.click();

            //get the output of a randomize action and see if this contains randomized
            String buttonText = driver.findElementByXPath("//*[@id=\"random-output\"]/div").getText();
            System.out.println(buttonText);
            boolean contains = buttonText.contains("randomized");
            assertTrue(contains, "Button press not successful");

            driver.quit();
        }
    }

    @Test
    public void listIsPresentAndRandomizedDrinkIsInList() throws InterruptedException, MalformedURLException {
        RemoteWebDriver chrome = new RemoteWebDriver(new URL("http://0.0.0.0:4444/wd/hub"), chromeCapabilities);
        RemoteWebDriver firefox = new RemoteWebDriver(new URL("http://0.0.0.0:4444/wd/hub"), firefoxCapabilities);

        List<RemoteWebDriver> drivers = new ArrayList<>();
        drivers.add(chrome);
        drivers.add(firefox);

        for (RemoteWebDriver driver : drivers) {
            driver.get("http://nodefrontend:5000");
            driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
            driver.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();
            TimeUnit.SECONDS.sleep(2);
            driver.findElement(By.id("randomize-button")).click();

            WebElement listOfDrinks = driver.findElement(By.xpath("//*[@id=\"getstarted\"]/div/div[4]/div/div/ul"));
            List<WebElement> webDrinks = listOfDrinks.findElements(By.tagName("li"));
            List<String> drinks = new ArrayList<>();
            for (int i = 0; i < webDrinks.size(); i++) {
                drinks.add(webDrinks.get(i).getText().toLowerCase());
            }

            TimeUnit.SECONDS.sleep(2);
            String randomizedDrink = driver.findElementByXPath("//*[@id=\"random-output\"]/div").getText();
            String[] splittedString = randomizedDrink.split(":");
            Assert.assertEquals("You have randomized", splittedString[0]);
            String formattedDrink = splittedString[1].toLowerCase().trim();
            boolean contains = drinks.contains(formattedDrink);
            assertTrue(contains, "Drink not in list");
        }
    }

}
