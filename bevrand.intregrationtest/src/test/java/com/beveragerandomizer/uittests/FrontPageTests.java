package com.beveragerandomizer.uittests;


import io.github.bonigarcia.SeleniumExtension;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;

import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SeleniumExtension.class)
public class FrontPageTests {

    @Test
    public void thenPageComesUp(ChromeDriver chrome) {
        chrome.get("http://www.beveragerandomizer.com/");
        chrome.manage().window().maximize();
        assertTrue(chrome.getTitle().startsWith("The Beverage Randomizer"));
    }

    @Test
    public void thenScrollButtonWorks(ChromeDriver chrome) throws InterruptedException {
        chrome.get("http://www.beveragerandomizer.com/");
        chrome.manage().window().maximize();
        chrome.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        chrome.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();
        chrome.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        TimeUnit.SECONDS.sleep(2);
        chrome.findElement(By.id("randomize-button")).click();
        TimeUnit.SECONDS.sleep(2);
    }
}
