<template>
    <div id="readablemain">
        <navbar></navbar>
        <header>
            <h2 id="personalSpaceUsername"></h2><br>
            <a href="#main"><img src="images/beerglass.png" height="125" width="125"/></a><br>

            <h3> Personal info</h3>
            <h4 id="usernamePersonal"> Username: </h4><br>

            <a onclick="addNewPlayList()" class="fa fa-plus-circle" style="font-size:32px;color:#09E983"><span class="label">Add playlist</span></a><br>
            <div class="notify"><span id="notifyType" class="">You already have a playlist with that name</span></div>

            <input type="text" placeholder="Playlist Name" id="playListCreationField"><br>


            <a class="button randomize" id="okPlayListCreation"><strong>Ok</strong></a>
            <a class="button randomize" id="cancelPlayListCreation"><strong>Cancel</strong></a>

            <ul class="nobull" id="personalPlaylists"> </ul>

        </header>
        <foot></foot>
    </div>
</template>

<script>
    import Footer from '../components/Footer.vue'
    import Navbar from "../components/Navbar.vue"

    export default {
        name: "profile",
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