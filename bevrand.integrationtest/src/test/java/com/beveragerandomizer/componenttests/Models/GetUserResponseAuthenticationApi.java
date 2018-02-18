package com.beveragerandomizer.componenttests.Models;

public class GetUserResponseAuthenticationApi {

    public String getUsername() {
        return username;
    }

    public String getEmailAddress() {
        return emailAddress;
    }

    public int getId() {
        return id;
    }

    public boolean isActive() {
        return active;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setEmailAddress(String emailAddress) {
        this.emailAddress = emailAddress;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public String username;
    public String emailAddress;
    public int id;
    public boolean active;
}
