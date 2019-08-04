<template>
    <div class="loginarea">
        <h2 id="personalSpaceUsername"></h2><br>
        <img src="../assets/images/beerglass.png" height="125" width="125"/><br>

        <h3> Personal info</h3>
        <h4 id="usernamePersonal"> Username: {{username}}</h4><br>

        <a class="hover-add"><font-awesome-icon v-on:click="addNewPlaylist" icon="plus-circle" size="2x" id='addPlayList'/><br>
        <span class="playlistaddition">Create Playlist</span></a><br>
        <br>

        <div v-for="(playlist, index) in playlists" :key="index" class="playlistcollapisble" id="playlists">
                <div class="collapsible"> {{ playlist.displayName }}
                    <a class="hover-edit" id="pencilbutton"><font-awesome-icon icon="pencil-alt" class="icons" v-on:click="editPlaylist(index)"/></a>
                    <a class="hover-delete" id="trashbutton"><font-awesome-icon icon="trash" class="icons" v-on:click="deletePlaylist(index)" /></a>
                    <a class="hover-play" id="dicebutton"><font-awesome-icon icon="dice" class="icons" v-on:click="playPlaylist(index)"/></a>
                    <a v-show="!playlists[index]['open']" class="hover-play">
                        <font-awesome-icon icon="arrow-alt-circle-down"
                         class="icons"
                         style="margin-left: 1em"
                         v-on:click="playlists[index]['open'] = !playlists[index]['open']"/></a>

                    <a v-show="playlists[index]['open']" class="hover-play">
                        <font-awesome-icon icon="arrow-alt-circle-up"
                            class="icons"
                            style="margin-left: 1em"
                            v-on:click="playlists[index]['open'] = !playlists[index]['open']"/></a>
                </div>
                <ul v-show="playlists[index]['open']">
                    <li v-for="beverage of playlist.beverages" >
                        {{ beverage }}
                    </li>
                </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "PlayListCreation",
        data() {
            return {
                username: this.$store.state.username,
                playlists: [],
                validName: false,
                validNameError: '',
                createdPlaylist: '',
                token: this.$store.state.token,
            }
        },

        methods: {
            getAllUserPlaylists: function () {
                return this.$apiClient.get(`${this.$proxyUrl}/playlist-api/v1/private/${this.username}`,
                    { headers: {"x-api-token": this.token} })
                .then((response) => {
                    let playlistArray = [];
                    response.data.result.forEach(function(resp) {
                        resp['open'] = false;
                        playlistArray.push(resp)
                    });
                    this.playlists = playlistArray;
                })
                .catch(e => {
                    this.errors.push(e)
                })
            },

            validateEnteredPlaylist: function(playlistName) {
                let normalizedName = playlistName.replace(/[^a-zA-Z0-9]/g, "");
                return this.$apiClient.get(`${this.$proxyUrl}/playlist-api/v1/private/${this.username}`,
                    { headers: {"x-api-token": this.token} })
                    .then((response) => {
                        response.data.result.forEach(function(resp) {
                            if (resp.displayName.toLowerCase() === playlistName.toLowerCase() ||
                                resp.list.toLowerCase() === normalizedName) {
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
            setPlaylistToParent: function (selectedPlayList) {
                this.$emit("setPlaylistToParent", selectedPlayList);
            },
            editPlaylist: function (index) {
                this.$router.push({name: 'editPlaylistPage', params: {
                        playlistDetail: this.playlists[index] }});
            },

            deletePlaylist: function (index) {
                this.$swal({
                    title: `Deleting ${this.playlists[index].displayName}`,
                    text: `Are you sure you want to delete ${this.playlists[index].displayName}?`,
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                 })
                    .then((willDelete) => {
                        if (willDelete) {
                            this.$apiClient({
                                method: "delete",
                                headers: {"x-api-token": this.token},
                                url: `${this.$proxyUrl}/playlist-api/v1/private/${this.username}/${this.playlists[index].list}`,
                                })
                                .then(response => {
                                    this.$swal(`${this.playlists[index].displayName} has been deleted`, {
                                        icon: "success",
                                    });
                                    this.playlists.splice(index, 1);
                                })
                                .catch(e => {
                                    this.$swal("Error", "Something went wrong", "error")
                                })
                        } else {
                            this.$swal(`Playlist ${this.playlists[index].displayName} was not deleted`);
                        }
                    });
            },
            playPlaylist: function (index) {
                this.$router.push({name: 'homepage', params: {playlist: this.playlists[index]}});
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
                        this.validNameError = 'Playlistname is empty or whitespace';
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