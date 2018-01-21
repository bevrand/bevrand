package com.beveragerandomizer.systemtests;

import com.beveragerandomizer.componenttests.Models.PostMongoApi;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import io.github.bonigarcia.SeleniumExtension;
import org.apache.xpath.SourceTree;
import org.json.JSONArray;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.phantomjs.PhantomJSDriver;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SeleniumExtension.class)
public class SystemTest {

    public static String reqUrlMongo;
    public static String reqUrlRandom;
    private static JSONArray userList;
    private static JSONArray frontpageList;
    private static PostMongoApi MongoModel;
    private static PostMongoApi updateMongoModel;
    private static PostMongoApi deleteMongoModel;

    @BeforeAll
    static void setParams() {
        reqUrlMongo = "http://0.0.0.0:4550/api/";
        reqUrlRandom = "http://0.0.0.0:4560/api/";
    }

    @Test
    void myFirstTest() {
        assertEquals(2, 1 + 1);
    }

    @Disabled
    @Test
    void getAllDrinksFromWebsiteAndCheckMongoApi(PhantomJSDriver driver){
        driver.get("http://0.0.0.0:4540");
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);
        driver.findElement(By.xpath("//*[@id='page-top']/header/div/div/a[1]")).click();

        WebElement listOfDrinks = driver.findElement(By.cssSelector("#about > div > div:nth-child(4) > div > ul"));
        List<WebElement> webDrinks = listOfDrinks.findElements(By.tagName("li"));
        List<String> drinks = new ArrayList<>();
        for (int i = 0; i < webDrinks.size(); i++)
        {
            drinks.add(webDrinks.get(i).getText().toLowerCase());
        }

        //Hard set to TGIF can be changed later to see if all lists work
        String bevUrl = reqUrlMongo + "frontpage?list=TGIF";
        JsonNode beveragesResponse = null;
        try {
            beveragesResponse = Unirest.get(bevUrl).asJson().getBody();
        } catch (UnirestException e) {
            e.printStackTrace();
        }
        Object beverageKey = beveragesResponse.getObject().keys().next();
        JSONArray beveragesMongo = beveragesResponse.getObject().getJSONArray(beverageKey.toString());
        assertTrue(beveragesMongo.length() > 0);


        List<String> mongoBeveragesNormalized = new ArrayList<String>();
        for (int i=0; i<beveragesMongo.length(); i++) {
            mongoBeveragesNormalized.add( beveragesMongo.getString(i).toLowerCase() );
        }

        for (int i = 0; i < drinks.size(); i++) {
            boolean contains = mongoBeveragesNormalized.contains(drinks.get(i));
            assertTrue(contains, "Drink not in list");
        }
    }
}


