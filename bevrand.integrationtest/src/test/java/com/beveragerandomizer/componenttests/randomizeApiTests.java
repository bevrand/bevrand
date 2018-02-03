package com.beveragerandomizer.componenttests;

import com.beveragerandomizer.componenttests.Models.DeleteResponseMongoApi;
import com.beveragerandomizer.componenttests.Models.PostMongoApi;
import com.beveragerandomizer.componenttests.Models.ReponseMongoApi;
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Assert;
import org.junit.jupiter.api.*;
import com.google.gson.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;



public class randomizeApiTests {

    public static String reqUrl;
    private static PostMongoApi MongoModel;


    @BeforeAll
    static void setParams() {
        reqUrl = "http://0.0.0.0:4560/api/";
    }

    @Test
    @DisplayName("Ping to see if service is on")
    void serviceIsOn() throws UnirestException {
        String url = "http://0.0.0.0:4560/ping";
        JsonNode response = Unirest.get(url).asJson().getBody();
        JSONObject json = response.getObject();
        Iterator<?> keys = json.keys();
        while (keys.hasNext()) {
            String key = keys.next().toString();
            String resString = response.getObject().getString(key);
            boolean message = key.equals("message");
            if (message) {
                Assert.assertEquals("pong!", resString);

            } else {
                Assert.assertEquals("success", resString);
            }
        }
    }

    @Disabled
    @Test
    @DisplayName("Post a number of drinks")
    void randomizeList()
    {
        MongoModel = new PostMongoApi();
        String user = "usertest";
        String list = "listtest";
        List<String> beverages = Arrays.asList("beer", "wine", "gin", "water", "tequilla");
        MongoModel.setUser(user);
        MongoModel.setList(list);
        MongoModel.setBeverages(beverages);

        Gson gson = new Gson();
        String json = gson.toJson(MongoModel);
        String url = reqUrl + "randomize";
        try {
            HttpResponse<JsonNode> response = Unirest.post(url)
                    .header("accept", "application/json")
                    .body(json)
                    .asJson();

            assertEquals(200, response.getStatus(), "Response not 200");


        } catch (UnirestException e) {
            e.printStackTrace();
            assertEquals(false, true);
        }

    }
}
