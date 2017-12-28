package com.beveragerandomizer.componenttests.Models;

import java.util.List;

public class PostMongoApi {
    public String getList() {
        return list;
    }

    public void setList(String list) {
        this.list = list;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public List<String> getBeverages() {
        return beverages;
    }

    public void setBeverages(List<String> beverages) {
        this.beverages = beverages;
    }

    public String list;
    public String user;
    public List<String> beverages;



}
