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
        <button v-on:click="filterList(searchTerm)">Filter</button>

        <br>

        <a class="hover-add"><font-awesome-icon v-on:click="addNewPlaylist" icon="plus-circle" size="2x"/><br>
        <span class="playlistaddition">Create Playlist</span></a><br>
        <br>
        <span v-for="(playlist, index) in playlists" :key="index" class="playlistcollapisble">
                <a class="collapsible" v-on:click="showItems = index"> {{playlist.displayName}}
                    <a class="hover-edit"><font-awesome-icon icon="pencil-alt" class="icons" v-on:click="editPlaylist(playlist)"/></a>
                    <a class="hover-delete"><font-awesome-icon icon="trash" class="icons" v-on:click="deletePlaylist(index)" /></a>
                    <a class="hover-play"><font-awesome-icon icon="dice" class="icons"/></a>
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
                this.$apiClient.get(`${this.$proxyUrl}/api/playlists?username=${this.username}`)
                    .then((response) => {
                        this.playlists = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },

            validateEnteredPlaylist: function(playlistName) {
                return this.$apiClient.get(`${this.$proxyUrl}/api/playlists?username=joeri&list=${playlistName}`)
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

            filterList: function (term) {
                let templist = []
                this.playlists.forEach(function(playlist) {
                    let matched = RegExp(`aa*`).test(playlist.displayName)
                    if (matched) {
                        console.log(playlist)
                        templist.push(playlist)
                    }
                });
                this.playlists = templist
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
        background-color: #B4B4B4;
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
        color: #ffffff;
        background-color: #B4B4B4;
        margin: 0.5em;
        display: block;
        text-align: center;
        padding: 1px;
        text-decoration: none;
        font-size: 1.5em;
    }

    .hover-add {
        margin-left: 1em;
        color: #68ff27;
        text-align: center;
    }

    .hover-delete {
        margin-left: 0.5em;
    }

    .hover-delete:hover {
        color: #ff271a;
    }

    .hover-edit {
        margin-left: 0.5em;
    }

    .hover-edit:hover {
        color: #3cfaff;
    }

    .hover-play {
        margin-left: 0.5em;
    }

    .hover-play:hover {
        color: #FF9500;
    }

</style>