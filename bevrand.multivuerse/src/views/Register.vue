<template>
    <div id="readablemain">
        <navbar></navbar>
        <h2 id="welcomeBannerText">Start your Adventure now!</h2>
        <h3 id="redirectionText">Redirecting you to your profile</h3>
        <h3 id="playlistCreationName"></h3><br>
        <form id="registrationForm"><br>

            <div class="notify"><span id="notifyType" class="">Something went wrong</span></div>
            <input type="email" placeholder="Email" id="emailField" required><br>
            <input type="text" autocomplete="false" id="usernameField" required  placeholder="Username"><br>
            <input type="password" placeholder="Password" id="passwordField" required><br>
            <input type="password" placeholder="Re-type Password" id="passwordVerificationField" required><br>

            <input type="submit" value="Sign up!" class="button randomize" id="registerButton">
        </form >
        <foot></foot>
    </div>
</template>

<script>
    import Footer from '../components/Footer.vue'
    import Navbar from "../components/Navbar.vue"

    export default {
        name: "register",
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
        padding: 4.5em 0 4.5em 0;
        margin-bottom: 0;
    }
</style>