<template>
    <div class="loginarea">
        <h2 id="personalSpaceUsername"></h2><br>
        <img src="../assets/images/beerglass.png" height="125" width="125"/><br>

        <h3> Personal info</h3>
        <h4 id="usernamePersonal"> Username: {{username}}</h4><br>

        <a onclick="addNewPlayList()" class="fa fa-plus-circle" style="font-size:32px;color:#09E983;cursor:pointer"><span class="playlistaddition">Add playlist</span></a><br>

        <floating-label
                :config="{
                label: 'Playlistname',
                name: 'playlistname',
                color: {
                  focusColor: '#ff9500',
                  lineColor: '#ff9500',
                  blurredColor: 'rgba(3, 23, 40, 0.34)'
                },
                hasClearButton: false
              }">
            <input type="text" class="inputfield" placeholder="Playlist Name" id="playListCreationField">
        </floating-label>
        </section>
        <br>
        <span v-for="(playlist, index) in playlists" :key="index" class="playlistcollapisble">
                <a class="collapsible" v-on:click="showItems = index"> {{playlist.displayName}}
                    <i style="margin-left: 0.5em;cursor:pointer"
                       class="fa fa-pencil"
                    v-on:click="editPlaylist(playlist)">
                    </i>
                    <i style="margin-left: 0.5em;cursor:pointer"
                       class="fa fa-trash"
                       v-on:click="deletePlaylist(index)"></i>
                </a>
                <ul id="beverageList" v-show="showItems === index">
                    <li v-for="beverage of playlist.beverages" >
                        {{ beverage }}
                    </li>
                </ul>
        </span>

    </div>
</template>

<script>
import FloatingLabel from "vue-simple-floating-labels";

    export default {
        name: "PlayListCreation",
        data() {
            return {
                username: this.$store.state.username,
                playlists: [],
                showItems: false
            }
        },

        methods: {
            getAllUserPlaylists: function () {
                this.$apiClient.get(`http://0.0.0.0:4540/api/playlists?username=joeri`)
                    .then((response) => {
                        this.playlists = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },

            editPlaylist: function (playlist) {
                this.$router.push({name: 'editPage', params: {info: playlist}});
            },

            deletePlaylist: function (index) {
                this.playlists.splice(index, 1);
            }
        },

        components: {
            FloatingLabel
        },

        mounted() {
            this.getAllUserPlaylists()
        },

    }
</script>

<style scoped>

    .inputarea {
        margin-top: 2em;
        margin-left: 22em;
        margin-right: 22em;
        text-align: center;
    }

    @media screen and (max-width: 1366px) {
        .inputarea {
            margin-top: 2em;
            margin-left: 10em;
            margin-right: 10em;
            text-align: center;
        }
    }

    @media screen and (max-width: 650px) {
        .inputarea {
            margin-top: 2em;
            margin-left: 1em;
            margin-right: 1em;
            text-align: center;
        }
    }

    .playlistaddition:hover {
        cursor: pointer;
    }

    .playlistcollapisble {
        background-color: #FF9500;
        margin-left: 20em;
        margin-right: 20em;
        margin-top: 2em;
        display: block;
        text-align: center;
        text-decoration: none;
        font-size: 1em;
    }

    @media screen and (max-width: 1366px) {
        .playlistcollapisble {
            margin-top: 2em;
            margin-left: 10em;
            margin-right: 10em;
            text-align: center;
        }
    }

    @media screen and (max-width: 650px) {
        .playlistcollapisble {
            margin-top: 2em;
            margin-left: 1em;
            margin-right: 1em;
            text-align: center;
        }
    }

    .collapsible {
        color: #fff;
        background-color: #FF9500;
        margin: 0.5em;
        display: block;
        text-align: center;
        padding: 1px;
        text-decoration: none;
        font-size: 1.5em;
    }

    .inputfield {
        font-family: "Ubuntu", sans-serif;
        margin: auto;
        display: block;
        padding: 5px;
        border: none;
        font-size: 16px;
        width: 8em;
    }

</style>