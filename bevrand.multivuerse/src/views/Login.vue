<template>
    <div id="readablemain">
        <navbar></navbar>
        <h2 id="welcomeBannerText">Welcome!</h2><br>
        <h3 id="redirectionText">Redirecting you to your profile</h3>
        <form id="loginForm">
            <div class="notify"><span id="notifyType" class="">Not a user</span></div>
            <input type="email" placeholder="Email" id="emailField"><br>
            <input type="text" autocomplete="false" id="usernameField" placeholder="Username"><br>
            <input type="password" placeholder="Password" id="passwordField"><br>

            <input type="submit" value="Login" class="button randomize" id="loginButton">

        </form>
        <div class="text-center p-t-115" id="signUpText">
            <span class="txt1" id="accountText">
                Don’t have an account?
            </span>
            <a class="txt2" href="register.html" id="registerLink">
                Sign Up
            </a>
        </div>
        <foot></foot>
    </div>
</template>

<script>
import Footer from '../components/Footer.vue'
import Navbar from "../components/Navbar.vue"

export default {
        name: "login",
        data () {
            return {}
        },

        components: {
            'navbar': Navbar,
            'foot': Footer
        },
    }
</script>

<style scoped>
    #readablemain {
        background-color: #7C7C7C;
        text-align: center;
    }
</style>