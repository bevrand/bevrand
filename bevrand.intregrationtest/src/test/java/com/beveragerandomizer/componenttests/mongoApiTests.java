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

public class mongoApiTests {


    public static String reqUrl;
    private static JSONArray userList;
    private static JSONArray frontpageList;
    private static PostMongoApi MongoModel;
    private static PostMongoApi updateMongoModel;
    private static PostMongoApi deleteMongoModel;

    @BeforeAll
    static void setParams() {
        reqUrl = "http://0.0.0.0:4550/api/";
    }

    @Test
    @DisplayName("Ping to see if service is on")
    void serviceIsOn() throws UnirestException {
        String url = "http://0.0.0.0:4550/ping";
        JsonNode response = Unirest.get(url).asJson().getBody();
        JSONObject json = response.getObject();
        Iterator<?> keys = json.keys();
        while (keys.hasNext()){
            String key = keys.next().toString();
            String resString = response.getObject().getString(key);
            boolean message = key.equals("message");
            if (message) {
                Assert.assertEquals("pong!", resString);

            }
            else {
                Assert.assertEquals("success", resString);
            }
        }


    }

    @Nested
    @DisplayName("Test for the frontpage")
    class FrontPageGet {

        @Test
        @DisplayName("Given I make a call for all frontpage users")
        void getAllFrontPageUsers() throws UnirestException {
            String url = reqUrl + "frontpage";
            JsonNode response = Unirest.get(url).asJson().getBody();
            String frontpageKey = response.getObject().keys().next().toString();
            frontpageList = response.getObject().getJSONArray(frontpageKey);
            assertTrue(frontpageList.length() > 0, "Frontpage is empty");
        }

        @Nested
        @DisplayName("When calling each frontpagelist")
        class InnerFrontpageGet {

            @Test
            @DisplayName("Then I check that there are beverage")
            void getAllInnerLists() throws UnirestException {
                for (int j = 0; j < frontpageList.length(); j++) {
                    String bevUrl = reqUrl + "frontpage?list=" + frontpageList.getString(j);
                    JsonNode beveragesResponse = Unirest.get(bevUrl).asJson().getBody();
                    Object beverageKey = beveragesResponse.getObject().keys().next();
                    JSONArray beverages = beveragesResponse.getObject().getJSONArray(beverageKey.toString());
                    assertTrue(beverages.length() > 0);
                }
            }
        }
    }


    @Nested
    @DisplayName("Test for the users")
    class UsersGet {

        @Test
        @DisplayName("Given I make a call for all users")
        void getAllUsers() throws UnirestException {
            String url = reqUrl + "users";
            JsonNode response = Unirest.get(url).asJson().getBody();
            userList = response.getObject().getJSONArray("users");
            assertTrue(userList.length() > 0, "UserList is empty");
        }

        @Nested
        @DisplayName("When calling each user list")
        class InnerUsersGet {

            @Test
            @DisplayName("Then I check the beverages")
            void getAllInnerLists() throws UnirestException {
                for (int i = 0; i < userList.length(); i++) {
                    String user = userList.getString(i);
                    String userUrl = reqUrl + "users?user=" + user;
                    JSONArray userResponse = Unirest.get(userUrl).asJson().getBody().getObject().getJSONArray("descriptions");
                    assertTrue(userResponse.length() > 0, "List field is empty");
                    for (int j = 0; j < userResponse.length(); j++) {
                        String bevUrl = userUrl + "&list=" + userResponse.getString(j);
                        JsonNode beveragesResponse = Unirest.get(bevUrl).asJson().getBody();
                        Object beverageKey = beveragesResponse.getObject().keys().next();
                        JSONArray beverages = beveragesResponse.getObject().getJSONArray(beverageKey.toString());
                        assertTrue(beverages.length() > 0);
                    }
                }
            }
        }
    }


    @Nested
    @DisplayName("Test for creating users")
    class UsersPost {


        @BeforeEach
        void createUserModel() {
            MongoModel = new PostMongoApi();
            String user = "usertest";
            String list = "listtest";
            List<String> beverages = Arrays.asList("beer", "wine", "gin", "water", "tequilla");
            MongoModel.setUser(user);
            MongoModel.setList(list);
            MongoModel.setBeverages(beverages);
        }


        @Test
        @DisplayName("When I post this model")
        void postUserModel() {
            Gson gson = new Gson();
            String json = gson.toJson(MongoModel);
            String url = reqUrl + "users";
            try {
                HttpResponse<JsonNode> response = Unirest.post(url).header("accept", "application/json")
                        .header("Content-Type", "application/json").body(json).asJson();
                assertEquals(200, response.getStatus(), "Response not 200");
                String moreJson = response.getBody().toString();
                ReponseMongoApi res = gson.fromJson(moreJson, ReponseMongoApi.class);
                assertEquals(MongoModel.user, res.user);
                assertEquals(MongoModel.list, res.list);
                assertEquals(MongoModel.list, res.newdata.list);
                assertTrue(res.message.contains("Your list with id:"));
            } catch (UnirestException e) {
                e.printStackTrace();
                assertTrue(false);
            }

        }

        @Test
        @DisplayName("Then I am not allowed to post it again")
        void postUserModelAgain() {
            Gson gson = new Gson();
            String json = gson.toJson(MongoModel);
            String url = reqUrl + "users";
            try {
                HttpResponse<JsonNode> response = Unirest.post(url).header("accept", "application/json")
                        .header("Content-Type", "application/json").body(json).asJson();
            } catch (UnirestException e) {
                assertTrue(true);
            }
        }

        @Nested
        @DisplayName("Test for getting the created user")
        class UsersPostInner {


            @Test
            @DisplayName("Then I get this model back with a get")
            void gettUserModel() throws UnirestException {
                String url = reqUrl + "users";
                JsonNode response = Unirest.get(url).asJson().getBody();
                JSONArray jsonResponse = response.getObject().getJSONArray("users");

                List<String> addedUserList = new ArrayList<>();
                for (int i = 0; i < jsonResponse.length(); i++) {
                    addedUserList.add(jsonResponse.getString(i));
                }

                boolean contains = addedUserList.contains(MongoModel.user);
                assertTrue(contains, "User was not added");
            }

            @Test
            @DisplayName("Then I get this model back with a get")
            void getBeveragesModel() throws UnirestException {
                String url = reqUrl + "users?user=" + MongoModel.user + "&list=" + MongoModel.list;

                JsonNode response = Unirest.get(url).asJson().getBody();
                Object beverageKey = response.getObject().keys().next();
                JSONArray beverages = response.getObject().getJSONArray(beverageKey.toString());
                assertTrue(beverages.length() > 0);

                List<String> beverageList = new ArrayList<>();
                for (int i = 0; i < beverages.length(); i++) {
                    beverageList.add(beverages.getString(i));
                }

                for (String beverage : beverageList) {
                    boolean contains = MongoModel.beverages.contains(beverage);
                    assertTrue(contains, "User was not added");
                }

            }
        }
    }

    @Nested
    @DisplayName("Test for updating users")
    class UsersPut {

        @BeforeEach
        void createUserModel() {
            updateMongoModel = new PostMongoApi();
            String user = "usertest";
            String list = "listtest";
            List<String> beverages = Arrays.asList("beer", "wine", "gin", "water", "tequilla");
            updateMongoModel.setUser(user);
            updateMongoModel.setList(list);
            updateMongoModel.setBeverages(beverages);
            Gson gson = new Gson();
            String json = gson.toJson(updateMongoModel);
            String url = reqUrl + "users";
            try {
                HttpResponse<JsonNode> response = Unirest.post(url).header("accept", "application/json")
                        .header("Content-Type", "application/json").body(json).asJson();
                assertEquals(200, response.getStatus(), "Response not 200");
            } catch (UnirestException e) {
                e.printStackTrace();
            }
        }

        @AfterEach
        void deleteUserModel() throws UnirestException {
            String url = reqUrl + "users?user=" + updateMongoModel.user + "&list=" + updateMongoModel.list;
            JsonNode response = Unirest.delete(url).asJson().getBody();
            Gson gson = new Gson();
            String json = response.toString();
            DeleteResponseMongoApi res = gson.fromJson(json, DeleteResponseMongoApi.class);
            assertEquals("No more data", res.newdata );
            assertEquals("Delete of 1 mongoobject(s) was successful", res.message);
        }

        @Test
        @DisplayName("Given I update the list")
        void putUserTest() {
            PostMongoApi updateMongo = new PostMongoApi();
            String user = "usertestupdate";
            String list = "listtestupdate";
            List<String> beverages = Arrays.asList("beer", "wine", "gin", "water", "tequilla", "anotherdrink");
            updateMongo.setUser(user);
            updateMongo.setList(list);
            updateMongo.setBeverages(beverages);
            Gson gson = new Gson();
            String json = gson.toJson(updateMongo);
            String url = reqUrl + "users?user=" + updateMongo.user + "&list=" + updateMongo.list;
            try {
                HttpResponse<JsonNode> response = Unirest.put(url).header("accept", "application/json")
                        .header("Content-Type", "application/json").body(json).asJson();
                assertEquals(200, response.getStatus());

                String urlUpdate = reqUrl + "users?user=" + updateMongo.user + "&list=" + updateMongo.list;
                JsonNode updateResponse = Unirest.get(urlUpdate).asJson().getBody();
                Object beverageKey = updateResponse.getObject().keys().next();
                JSONArray updateBeverages = updateResponse.getObject().getJSONArray(beverageKey.toString());
                assertTrue(updateBeverages.length() > 0);

                List<String> beverageList = new ArrayList<>();
                for (int i = 0; i < updateBeverages.length(); i++) {
                    beverageList.add(updateBeverages.getString(i));
                }

                for (String beverage : beverageList) {
                    boolean contains = updateMongo.beverages.contains(beverage);
                    assertTrue(contains, "User was not added");
                }

            } catch (UnirestException e) {
                assertTrue(true);
            }
        }
    }

    @Nested
    @DisplayName("Test for deleting users")
    class UsersDelete {

        @BeforeEach
        void createUserModel() {
            deleteMongoModel = new PostMongoApi();
            String user = "deletetest";
            String list = "deletetest";
            List<String> beverages = Arrays.asList("beer", "wine", "gin", "water", "tequilla");
            deleteMongoModel.setUser(user);
            deleteMongoModel.setList(list);
            deleteMongoModel.setBeverages(beverages);
            Gson gson = new Gson();
            String json = gson.toJson(deleteMongoModel);
            String url = reqUrl + "users";
            try {
                HttpResponse<JsonNode> response = Unirest.post(url).header("accept", "application/json")
                        .header("Content-Type", "application/json").body(json).asJson();
                assertEquals(200, response.getStatus(), "Response not 200");
            } catch (UnirestException e) {
                e.printStackTrace();
            }
        }

        @AfterEach
        void deleteUser() {
        }

        @Test
        @DisplayName("Given I delete the list")
        void deleteUserModel() {
            String url = reqUrl + "users?user=" + deleteMongoModel.user + "&list=" + deleteMongoModel.list;
            try {
                JsonNode response = Unirest.delete(url).asJson().getBody();
                Gson gson = new Gson();
                String json = response.toString();
                DeleteResponseMongoApi res = gson.fromJson(json, DeleteResponseMongoApi.class);
                assertEquals(deleteMongoModel.user, res.user);
                assertEquals(deleteMongoModel.list, res.list);
                assertEquals("No more data", res.newdata );
                assertEquals("Delete of 1 mongoobject(s) was successful", res.message);
            } catch (UnirestException e) {
                e.printStackTrace();
            }
        }
    }


    @AfterAll
    static void deleteUserModel() throws UnirestException {
        String url = reqUrl + "users?user=" + MongoModel.user + "&list=" + MongoModel.list;
        JsonNode response = Unirest.delete(url).asJson().getBody();
        Gson gson = new Gson();
        String json = response.toString();
        DeleteResponseMongoApi res = gson.fromJson(json, DeleteResponseMongoApi.class);
        assertEquals("No more data", res.newdata );
        assertEquals("Delete of 1 mongoobject(s) was successful", res.message);

    }

}







/*

 */