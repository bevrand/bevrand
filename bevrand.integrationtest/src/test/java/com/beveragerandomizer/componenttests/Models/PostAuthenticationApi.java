package com.beveragerandomizer.componenttests.Models;


public class PostAuthenticationApi {
    public String getUsername() {
        return username;
    }

    public String getEmailAddress() {
        return emailAddress;
    }

    public String getPassWord() {
        return passWord;
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

    public void setPassWord(String passWord) {
        this.passWord = passWord;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public String username;
    public String emailAddress;
    public String passWord;
    public boolean active;
}





