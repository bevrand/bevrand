package com.beveragerandomizer.componenttests.Models;

public class ReponseMongoApi {

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public String getList() {
        return list;
    }

    public void setList(String list) {
        this.list = list;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public PostMongoApi getNewdata() {
        return newdata;
    }

    public void setNewdata(PostMongoApi newdata) {
        this.newdata = newdata;
    }

    public String user;
    public String list;
    public String message;
    public PostMongoApi newdata;

}
