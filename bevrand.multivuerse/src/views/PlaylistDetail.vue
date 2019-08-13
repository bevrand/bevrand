<template>
    <div id="playlistDetaild" class="playlistcreation">
        <navbar></navbar>
        <div id="creationArea" class="creationfield">
            <span class="label">
                <a class="image featured" ><img :src="imageUrl" ></a><br>
                <a class="playlistselector" id="playlistName"><h3> Playlist: {{ displayName }}</h3>  </a>
                <h3 style="margin-bottom: 0.5em">Beverages:</h3><br>
                <ul id="detailedBeverages">
                    <li v-for="beverage of beverages" >
                        {{ beverage }}
                    </li>
                </ul>
                 <a class="hover-play" id="dicebutton"><font-awesome-icon  icon="dice" class="icons" size="2x"
                                                                           v-on:click="playPlaylist()"/></a>
                 <a class="hover-edit" id="pencilbutton"><font-awesome-icon icon="pencil-alt" class="icons" size="2x"
                                                                            v-if="loggedIn" v-on:click="editPlaylist()"/></a>
            </span>
            <span class="highscores">
            <h3 style="margin-bottom: 0.5em" v-if="globalHighScores.length > 2">Global Highscore:</h3>
                <table>
                    <tbody id="globalHighscore" v-if="globalHighScores.length > 2">
                        <tr>
                            <th><strong>Rank</strong></th>
                            <th><strong>Beverage</strong></th>
                            <th><strong>Rolled</strong></th>
                        </tr>
                        <tr v-for="(highscore, index) in globalHighScores"
                            :key="index" >
                            <td>{{ index + 1 }}</td>
                            <td>{{ highscore.drink }}</td>
                            <td>{{ highscore.rolled }}</td>
                        </tr>
                  </tbody>
                </table>
            <h3 style="margin-bottom: 0.5em" v-if="playlistHighScores.length > 2">Playlist Highscore:</h3>
                <table>
                    <tbody id="playlistHighscore"  v-if="playlistHighScores.length > 2">
                        <tr>
                            <th><strong>Rank</strong></th>
                            <th><strong>Beverage</strong></th>
                            <th><strong>Rolled</strong></th>
                        </tr>
                        <tr v-for="(highscore, index) in playlistHighScores"
                            :key="index" >
                            <td> {{ index + 1 }}</td>
                            <td>{{ highscore.drink }}</td>
                            <td>{{ highscore.rolled }}</td>
                        </tr>
                  </tbody>
                </table>
            </span>
        <foot></foot>
    </div>
    </div>
</template>


<script>
    import Footer from "../components/Footer.vue"
    import Navbar from "../components/Navbar.vue"

    export default {
        name: 'PlaylistDetail',
        data() {
            return {
                loggedIn: this.$store.state.loggedIn,
                errors: [],
                globalHighScores: [],
                playlistHighScores: [],
                displayName: this.$route.params.playlistDetail.displayName,
                beverages:this.$route.params.playlistDetail.beverages,
                imageUrl: this.$route.params.playlistDetail.imageUrl,
                playlistName: this.$route.params.playlistDetail.list,
                username: this.$route.params.playlistDetail.user,
            };
        },
        mounted() {
            window.scrollTo(0,0);
            this.getHighScores();
        },
        created() {
        },
        methods: {
            playPlaylist: function () {
                this.$router.push({name: 'homepage', params: {playlist: this.$route.params.playlistDetail}});
            },
            editPlaylist: function () {
                this.$router.push({name: 'editPlaylistPage', params: {
                        playlistDetail: this.$route.params.playlistDetail }});
            },
            getHighScores: function () {
                this.$apiClient.get(`${this.$proxyUrl}/highscore-api/v1/highscores`)
                    .then((response) => {
                        let highscores = 0;
                        if(response.data.length > 3) {
                            highscores = response.data.slice(0, 3)
                        }
                        else {
                            highscores = response.data
                        }
                        this.globalHighScores = highscores;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                this.$apiClient.get(`${this.$proxyUrl}/highscore-api/v1/highscores/${this.username}/${this.playlistName}`)
                    .then((response) => {
                        let highscores = 0;
                        if(response.data.length > 3) {
                            highscores = response.data.slice(0, 3)
                        }
                        else {
                            highscores = response.data
                        }
                        this.playlistHighScores = highscores;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
            },
        },
        components: {
            'navbar': Navbar,
            'foot': Footer,
        },
    };
</script>

<style scoped>
    .playlistcreation {
        background-color: #7A2F9E;
        text-align: center;
    }

    .image {
        position: relative;
        display: inline-block;
        border: 0;
        outline: 0;
    }

    .image img {
        display: block;
        width: 40%;
        height: 40%;
    }

    .image.featured {
        display: block;
        margin: 0 0 0 0;
        cursor: pointer;
    }

    ul {
        list-style-type: none;
    }

    .label {
        position: relative;
        top: 0;
        width: auto;
    }

    .label .image {
        position: relative;
        width: 65%;
        height: auto;
        margin-top: 2em;
        margin-left: 37%;
        margin-bottom: 1em;
    }

    @media screen and (max-width: 1366px) {
        .label .image {
            position: relative;
            width: 75%;
            height: auto;
            margin-top: 2em;
            margin-left: 30%;
            margin-bottom: 0.5em;
        }
    }

    @media screen and (max-width: 650px) {
        .label .image {
            position: relative;
            margin-top: 1em;
            margin-left: 30%;
            margin-bottom: 0.25em;
        }
    }

    .label h3 {
        margin-bottom: 1em;
        font-size: 1.5em;
        cursor: pointer;
        font-weight: bold;
        text-align: center;
    }

    .hover-play {
        margin-left: 0.5em;
    }

    .hover-play:hover {
        color: #FF9500;
    }

    .highscores h3 {
        margin-top: 0.5em;
        margin-bottom: 1em;
        font-size: 1.5em;
        cursor: pointer;
        font-weight: bold;
        text-align: center;
    }

    .highscores table {
        color: white;
        border-radius: 10px;
        border-spacing: 0;
        position: relative;
        width: auto;
        height: auto;
        margin-top: 2em;
        margin-left: 40%;
        margin-bottom: 1.5em;
    }

    @media screen and (max-width: 1366px) {
        .highscores table {
            position: relative;
            width: 60%;
            height: auto;
            margin-top: 2em;
            margin-left: 20%;
            margin-bottom: 1em;
        }
    }

    @media screen and (max-width: 400px) {
        .highscores table {
            position: relative;
            font-size: medium;
            width: 40%;
            margin-left: 12%;
            margin-top: 2em;
            margin-bottom: 1em;
        }
    }

    .highscores tr:first-child{
        background-color: #20b2aa;
    }

    .highscores tr:nth-child(2) > td{
        background-color: #ff9500;
        border-top-width: 0;
    }
    .highscores tr:nth-child(3) > td{
        background-color: #ffa01a;
        border-top-width: 0;
    }
    .highscores tr:nth-child(4) > td{
        background-color: #ffab34;
        border-top-width: 0;
    }

    .highscores th, td{
        padding: .5em 1.5em;
        text-align: center;
        border-style: solid;
    }
    .circledbutton{
        position: relative;
        height: 3em;
        margin-left: 0.5em;
        margin-bottom: 0.5em;
        width: 12em;
        font-size:13px;
        font-family:arial, helvetica, sans-serif;
        padding: 10px 10px 10px 10px;
        text-shadow: -1px -1px 0 rgba(0,0,0,0.3);
        font-weight:bold;
        text-align: center;
        color: #FFFFFF;
        background-color: #FF9500;
    }

    .circledbutton:hover{
        background: #7A2F9E;
    }

    .submitbutton {
        position: relative;
        display: inline-block;
        background: #ff9500;
        color: #ffffff;
        text-align: center;
        border-radius: 0.5em;
        text-decoration: none;
        padding: 0.65em 3em 0.65em 3em;
        margin-top: 2em;
        margin-bottom: 2em;
        cursor: pointer;
        outline: 0;
        font-weight: 400;
        font-size: 1em;
        font-family: "Ubuntu", sans-serif;
        -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
        -webkit-transition: background-color 0.35s ease-in-out,
        color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
        transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
    }

    .submitbutton:hover {
        color: #fff;
        background: #424242;
        letter-spacing: 1px;
        -webkit-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
        -moz-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
        box-shadow: 5px 40px -10px rgba(0, 0, 0, 0.57);
        transition: all 0.4s ease 0s;
    }

</style>

