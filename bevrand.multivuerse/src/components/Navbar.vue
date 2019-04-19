<template>
    <div id="navbar">
        <main id="page-wrap" class="navbar">
            <Slide>
                <router-link
                        tag="a"
                        id="headerLink"
                        class="navbar-header"
                        :to="{ name: 'homepage' }">
                    Bevrand
                </router-link>
                <router-link
                        tag="a"
                        v-if="!isLoggedIn"
                        id="navlinkLogin"
                        :to="{ name: 'loginPage' }">
                    Login
                </router-link>
                <router-link
                        tag="a"
                        v-if="!isLoggedIn"
                        id="navlinkRegister"
                        :to="{ name: 'registerPage' }">
                    Register
                </router-link>
                <router-link
                        tag="a"
                        v-if="isLoggedIn"
                        id="navlinkProfile"
                        :to="{ name: 'profilePage' }">
                    Profile
                </router-link>
                <a
                        v-on:click="logoutUser"
                        v-if="isLoggedIn"
                        id="navlinkLogout">
                    Logout
                </a>
            </Slide>
        </main>
    </div>
</template>

<script>
import { Slide } from 'vue-burger-menu'

    export default {
        name: "Navbar",
        data() {
            return {
                isLoggedIn: this.$store.state.loggedIn
            }
        },
        components: {
            Slide
        },
        methods: {
            logoutUser: function () {
                this.$store.commit('logOut');
                this.$router.push({ name: 'loginPage' });
            }
        },
    }

</script>

<style>

    #navbar {
        height: 3em;
        background-color: #FF9500;
    }

    a {
        cursor: pointer;
    }

    /* Navbar links */
    .navbar-header {
        float: left;
        margin: 0.5em;
        display: block;
        color: #f2f2f2;
        text-align: center;
        padding: 4px;
        text-decoration: none;
        text-transform: uppercase;
        font-weight: bold;
        font-size: 2em;
    }

    .bm-burger-button {
        position: fixed;
        width: 36px;
        height: 30px;
        left: 16px !important;
        top: 16px !important;
        cursor: pointer;
    }

    .bm-burger-bars {
        background-color: #373a47;
    }
    .line-style {
        position: absolute;
        height: 20%;
        left: 0;
        right: 0;
    }
    .cross-style {
        position: absolute;
        top: 12px;
        right: 2px;
        cursor: pointer;
    }
    .bm-cross {
        background: #bdc3c7;
    }
    .bm-cross-button {
        height: 24px;
        width: 24px;
    }
    .bm-menu {
        height: 100%; /* 100% Full-height */
        width: 0; /* 0 width - change this with JavaScript */
        position: fixed; /* Stay in place */
        z-index: 1000; /* Stay on top */
        top: 0;
        left: 0;
        background-color: rgb(63, 63, 65); /* Black*/
        overflow-x: hidden; /* Disable horizontal scroll */
        padding-top: 60px; /* Place content 60px from the top */
        transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
    }

    .bm-overlay {
        background: rgba(0, 0, 0, 0.3);
    }
    .bm-item-list {
        color: #b8b7ad;
        margin-left: 10%;
        font-size: 20px;
    }
    .bm-item-list > * {
        display: flex;
        text-decoration: none;
        padding: 0.7em;
    }
    .bm-item-list > * > span {
        margin-left: 10px;
        font-weight: 700;
        color: white;
    }

</style>