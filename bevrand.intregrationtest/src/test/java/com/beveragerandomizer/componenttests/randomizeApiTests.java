package com.beveragerandomizer.componenttests;

import com.beveragerandomizer.componenttests.Models.PostMongoApi;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Assert;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Iterator;

import static org.junit.jupiter.api.Assertions.assertEquals;



public class randomizeApiTests {

    public static String reqUrl;
    private static JSONArray userList;
    private static JSONArray frontpageList;


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
}
