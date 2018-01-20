package com.beveragerandomizer.uittests;


import io.github.bonigarcia.SeleniumExtension;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.phantomjs.PhantomJSDriver;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SeleniumExtension.class)
public class FrontPageTests {

    /*
    @Test
    public void testWithChrome()
    {
        final ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.setBinary("/path/to/google-chrome-stable");
        chromeOptions.addArguments("--headless");
        chromeOptions.addArguments("--disable-gpu");

        final DesiredCapabilities dc = new DesiredCapabilities();
        dc.setJavascriptEnabled(true);
        dc.setCapability(
                ChromeOptions.CAPABILITY, chromeOptions
        );

        WebDriver chrome = new ChromeDriver(dc);
        chrome.get("http://0.0.0.0:4540");
        chrome.manage().window().maximize();
        assertTrue(chrome.getTitle().startsWith("The Beverage Randomizer"));
    }
    */

    @Test
    public void pageComesUpAndHasCorrectTitle(PhantomJSDriver driver) {
        driver.get("http://0.0.0.0:4540");
        driver.manage().window().maximize();
        assertTrue(driver.getTitle().startsWith("The Beverage Randomizer"));
    }

    @Test
    public void thenScrollButtonWorks(PhantomJSDriver driver) throws InterruptedException {
        driver.get("http://0.0.0.0:4540");
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        driver.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        TimeUnit.SECONDS.sleep(2);
        driver.findElement(By.id("randomize-button")).click();
    }

    @Test
    public void listIsPresentAndRandomizedDrinkIsInList(PhantomJSDriver driver) throws InterruptedException {
        driver.get("http://0.0.0.0:4540");
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        driver.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        TimeUnit.SECONDS.sleep(2);
        driver.findElement(By.id("randomize-button")).click();

        WebElement listOfDrinks = driver.findElement(By.cssSelector("#about > div > div:nth-child(4) > div > ul"));
        List<WebElement> webDrinks = listOfDrinks.findElements(By.tagName("li"));
        List<String> drinks = new ArrayList<>();
        for (int i = 0; i < webDrinks.size(); i++)
        {
            drinks.add(webDrinks.get(i).getText().toLowerCase());
        }

        TimeUnit.SECONDS.sleep(2);
        String randomizedDrink = driver.findElement(By.cssSelector("#random-output > div")).getText();
        String[] splittedString = randomizedDrink.split(":");
        Assert.assertEquals("You randomized", splittedString[0]);
        String formattedDrink = splittedString[1].toLowerCase().trim();
        boolean contains = drinks.contains(formattedDrink);
        assertTrue(contains, "Drink not in list");
    }
}
