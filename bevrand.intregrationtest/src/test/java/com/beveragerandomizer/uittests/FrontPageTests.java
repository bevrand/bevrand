package com.beveragerandomizer.uittests;


import io.github.bonigarcia.SeleniumExtension;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.phantomjs.PhantomJSDriver;
import org.openqa.selenium.remote.DesiredCapabilities;

import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SeleniumExtension.class)
public class FrontPageTests {

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

    @Test
    public void thenPageComesUp(PhantomJSDriver phantom) {
        phantom.get("http://0.0.0.0:4540");
        phantom.manage().window().maximize();
        assertTrue(phantom.getTitle().startsWith("The Beverage Randomizer"));
    }

    @Test
    public void thenScrollButtonWorks(PhantomJSDriver phantom) throws InterruptedException {
        phantom.get("http://0.0.0.0:4540");
        phantom.manage().window().maximize();
        phantom.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        phantom.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();
        phantom.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        TimeUnit.SECONDS.sleep(2);
        phantom.findElement(By.id("randomize-button")).click();

    }
}
