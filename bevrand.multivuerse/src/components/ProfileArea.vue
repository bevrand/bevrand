<template>
    <div class="loginarea">
        <h2 id="personalSpaceUsername"></h2><br>
        <img src="../assets/images/beerglass.png" height="125" width="125"/><br>

        <h3> Personal info</h3>
        <h4 id="usernamePersonal"> Username: {{username}}</h4><br>

        <label for="site-search">Filter playlists: </label>
        <input v-model="searchTerm" type="search" id="site-search" name="q"
               aria-label="Search through site content">
        <br>
        <a>Filtering on: {{ searchTerm }}</a>
        <button v-on:click="filterList">Filter</button>

        <br>

        <a v-on:click="addNewPlaylist" class="fa fa-plus-circle" style="font-size:32px;color:#09E983;cursor:pointer"><br>
        <span class="playlistaddition">Add playlist</span></a><br>
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
    export default {
        name: "PlayListCreation",
        data() {
            return {
                username: this.$store.state.username,
                playlists: [],
                filteredList: [],
                showItems: false,
                validName: false,
                validNameError: '',
                createdPlaylist: '',
                searchTerm: ''
            }
        },

        methods: {
            getAllUserPlaylists: function () {
                this.$apiClient.get(`http://0.0.0.0:4540/api/playlists?username=${this.username}`)
                    .then((response) => {
                        this.playlists = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },

            validateEnteredPlaylist: function(playlistName) {
                return this.$apiClient.get(`http://0.0.0.0:4540/api/playlists?username=joeri&list=${playlistName}`)
                    .then((response) => {
                        response['data'].forEach(function(resp) {
                            if (resp.displayName.toLowerCase() === playlistName.toLowerCase()) {
                                this.validName = false;
                                this.validNameError = 'Playlistname already exists'
                            }
                        });

                        this.validName = true
                    })
                    .catch(e => {
                        this.validName = false;
                        this.validNameError = 'This playlist already exists'
                    })
            },

            editPlaylist: function (playlist) {
                this.$router.push({name: 'editPage', params: {info: playlist}});
            },

            filterList: function () {
                let somethhing = this.playlists.forEach(function(resp) {

                    let what = RegExp('es*').test(resp.displayName)
                    if(what) {
                        console.log(resp)
                    }
                })
                console.log(somethhing)
            },

            deletePlaylist: function (index) {
                this.playlists.splice(index, 1);
            },
            async addNewPlaylist () {
                this.$swal({
                    text: 'Enter a playlist',
                    content: "input",
                    placeholder: "Playlist name",
                    buttons: {
                        cancel: true,
                        confirm: {
                            text: "Create!",
                            closeModal: true,
                        },
                        },
                    })
                .then(async value => {
                    if (value == null) {
                        this.$swal.stopLoading();
                        this.$swal.close()
                    }
                    else if (value.trim() === '') {
                        this.validName = false;
                        this.validNameError = 'Playlistname is empty or whitespace'
                        this.$swal(this.validNameError).then(() => {
                            this.addNewPlaylist()
                        })
                    }
                    else {
                        await this.validateEnteredPlaylist(value);
                        if (this.validName) {
                            this.$swal("Validation", "Time to get some drinks!", "success").then(() => {
                                let capDisplayName = value.charAt(0).toUpperCase() + value.slice(1);
                                this.$router.push({ name: 'playlistCreationPage', params: { displayName: capDisplayName} });
                            });
                        } else {
                            this.$swal(this.validNameError).then(() => {
                                this.addNewPlaylist()
                            })
                        }
                    }
                })
            },
        },

        components: {
        },

        mounted() {
            this.getAllUserPlaylists()
        },

    }
</script>

<style>

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

</style>