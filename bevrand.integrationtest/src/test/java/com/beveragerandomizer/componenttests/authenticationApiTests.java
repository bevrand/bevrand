package com.beveragerandomizer.componenttests;

import com.beveragerandomizer.componenttests.Models.PostAuthenticationApi;
import com.beveragerandomizer.componenttests.Models.ReponseAuthenicationApi;
import com.beveragerandomizer.componenttests.Models.GetUserResponseAuthenticationApi;
import com.google.gson.Gson;
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.JSONArray;
import org.junit.AfterClass;
import org.junit.jupiter.api.*;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class authenticationApiTests {

    private static String reqUrl;
    private static int PostedId;
    private static PostAuthenticationApi PostModel;

    @BeforeAll
    static void setParams() {
        reqUrl = "http://0.0.0.0:4570/api/";
    }

    @Nested
    @DisplayName("Test for the User controller")
    class UserControllerTest {

        @BeforeEach
        void createUserModel() {
            PostModel = new PostAuthenticationApi();
            String username = "bevrand";
            String password = "bevrand";
            String emailAddress = "bevrand@bevrand.nl";
            Boolean active = true;

            PostModel.setUsername(username);
            PostModel.setPassWord(password);
            PostModel.setEmailAddress(emailAddress);
            PostModel.setActive(active);
        }

        @AfterClass
        @DisplayName("Then I delete the list")
        void deleteUserModel() {
            String url = reqUrl + "user?Id=" + PostedId;
            try {
                HttpResponse<JsonNode> response = Unirest.delete(url).asJson();
                Gson gson = new Gson();
                String json = response.toString();
                assertEquals(200, response.getStatus());
            } catch (UnirestException e) {
                e.printStackTrace();
            }
        }

        @Test
        @DisplayName("Given I Post a user")
        void createdAUser() throws UnirestException {
            String url = reqUrl + "user";
            Gson gson = new Gson();
            String json = gson.toJson(PostModel);

            try {
                HttpResponse<JsonNode> response = Unirest.post(url).header("accept", "application/json")
                        .header("Content-Type", "application/json").body(json).asJson();
                assertEquals(200, response.getStatus(), "Response not 200");
                String jsonReponse = response.getBody().toString();
                ReponseAuthenicationApi returnedUser = gson.fromJson(jsonReponse, ReponseAuthenicationApi.class);
                assertEquals(returnedUser.username, PostModel.username);
                PostedId = returnedUser.id;

            } catch (UnirestException e) {
                e.printStackTrace();
                assertTrue(false);
            }
        }

            @Nested
            @DisplayName("Test for getting the created user")
            class UsersPostInner {


                @Test
                @DisplayName("When I get the user the data should match")
                void getAUser() throws UnirestException {
                    String url = reqUrl + "user?Id=" + PostedId;
                    Gson gson = new Gson();
                    HttpResponse<JsonNode>  response = Unirest.get(url).asJson();
                    String jsonReponse = response.getBody().toString();
                    GetUserResponseAuthenticationApi returnedUser = gson.fromJson(jsonReponse, GetUserResponseAuthenticationApi.class);
                    assertEquals(returnedUser.username, PostModel.username);
                    assertEquals(returnedUser.emailAddress, PostModel.emailAddress);
                    assertEquals(returnedUser.active, PostModel.active);
                }

            }




    }

}
