<template>
    <div class="navbar">
        <router-link
                tag="a"
                id="headerLink"
                class="navbar-header"
                :to="{ name: 'homepage' }">
            Bevrand
        </router-link>
    <nav id="iconSideBar" class="sidebar">
        <a href="javascript:void(0)" class="closebtn" v-on:click="closeNavbar">×</a>
        <router-link
                tag="a"
                id="navlinkLogin"
                :to="{ name: 'loginPage' }">
            Login
        </router-link>
        <router-link
                tag="a"
                id="navlinkRegister"
                :to="{ name: 'registerPage' }">
            Register
        </router-link>
        <router-link
                tag="a"
                id="navlinkProfile"
                :to="{ name: 'profilePage' }">
            Profile
        </router-link>
        <a id="navlinkLogout">Logout</a>
    </nav>
    <a class="fa fa-user fa-2x navbar-icon" id="userIconNavbar" v-on:click="openNavbar"></a>
    </div>
</template>

<script>
    export default {
        name: "Navbar",
        data() {
            return {
            }
        },
        methods: {
            openNavbar: function () {
                document.getElementById("iconSideBar").style.width = "15em";
            },
            closeNavbar: function () {
                document.getElementById("iconSideBar").style.width = "0";
            }
        },
    }

</script>

<style scoped>

    /* Style the navbar */
    .navbar {
        overflow: hidden;
        background-color: #FF9500;
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

    .navbar-icon {
        float: right;
        margin: 0.5em;
        display: block;
        color: #f2f2f2;
        text-align: center;
        padding: 4px;
        text-decoration: none;
    }

    /* The sticky class is added to the navbar with JS when it reaches its scroll position */
    .sticky {
        position: fixed;
        top: 0;
        width: 100%;
    }

    /* Add some top padding to the page content to prevent sudden quick movement (as the navigation bar gets a new position at the top of the page (position:fixed and top:0) */
    .sticky + .content {
        padding-top: 60px;
    }

    @media (max-width: 992px) {
        .alert-validate::before {
            visibility: visible;
            opacity: 1;
        }
    }

    .fa:hover {
        cursor: pointer;
    }

    .sidebar {
        height: 30%;
        width: 0;
        position: fixed;
        z-index: 999;
        top: 0;
        right: 0;
        background-color: #424242;
        overflow-x: hidden;
        transition: 0.5s;
        padding-top: 60px;
    }

    .sidebar a {
        padding: 8px 8px 8px 32px;
        text-decoration: none;
        font-size: 25px;
        color: #f1f1f1;
        display: block;
        transition: 0.3s;
    }

    .sidebar a:hover {
        color: #818181;
    }

    .sidebar .closebtn {
        position: absolute;
        top: 0;
        right: 25px;
        font-size: 36px;
        margin-left: 50px;
    }
</style>