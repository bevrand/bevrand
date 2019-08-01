<template>
    <!-- Carousel -->
        <carousel :perPageCustom="[[320, 1], [768, 2], [1024, 3]]"
                  :loop="true"
                  :mouseDrag="true" id="playlistCarousel">
            <slide v-for="playlist of playlists">
                <span class="label">
                <a class="image featured" href="#main" v-smooth-scroll="{ duration: 1000 }" v-on:click="setPlaylistToParent(playlist)"><img :src="playlist.imageUrl" ></a>
                <a class="playlistselector" href="#main" v-smooth-scroll="{ duration: 1000 }" v-on:click="setPlaylistToParent(playlist)" id="playlistName"><h3>{{ playlist.displayName }}</h3>  </a>
                <a class="hover-play" id="dicebutton" href="#main" v-smooth-scroll="{ duration: 1000 }"><font-awesome-icon  icon="dice" class="icons" size="2x" v-on:click="setPlaylistToParent(playlist)"/></a>
                    <ul id="beverageList">
                    <li v-for="beverage of playlist.beverages.slice(0, 6)" >
                        {{ beverage }}
                    </li>
                    <li>
                    <router-link
                        tag="button"
                        id="linkToAllDrinks"
                        class="showAllButton"
                        :to="{ name: 'playlistDetailPage', params: {
                                                playlistDetail: playlist }}">
                    Show me all drinks!
                    </router-link>
                    </li>
                </ul>
                </span>
            </slide>
            <slide v-if="!loggedIn">
                <span class="label">
                    <router-link :to="{ name: 'loginPage' }">
                    <a class="image featured"><img src="../assets/images/header02.jpg"></a>
                    </router-link>
                    <router-link
                            tag="h3"
                            id="LoginAndRegister"
                            :to="{ name: 'loginPage' }">
                    Create your own playlist
                    </router-link>
                    <a>In order to create your own playlists you need to be registered</a>
                </span>
            </slide>
            <slide v-if="loggedIn">
                <span class="label">
                    <router-link :to="{ name: 'profilePage' }">
                    <a class="image featured"><img src="../assets/images/header02.jpg"></a>
                    </router-link>
                    <router-link
                            tag="h3"
                            id="LoginAndRegister"
                            :to="{ name: 'profilePage' }">
                    Create more playlists!
                    </router-link>
                </span>
            </slide>

</carousel>
</template>

<script>
import { Carousel, Slide } from 'vue-carousel';

    export default {
        name: "PlaylistSelection",
        data() {
            return {
                playlists: [],
                errors: [],
                username: this.$store.state.username,
                loggedIn: this.$store.state.loggedIn,
                token: this.$store.state.token,
            }
        },
        created() {

        },
        methods: {
            getAllPlaylists: function () {
                this.$apiClient.get(`${this.$proxyUrl}/playlist-api/v2/frontpage`)
                        .then((response) => {
                            this.playlists = response.data;
                            if (this.$parent.selectedPlaylist === null) {
                                this.setPlaylistToParent(response.data[0])
                            }
                        })
                        .catch(e => {
                            this.errors.push(e)
                        })
                },
            getAllUserPlaylists: function () {
                this.$apiClient.get(`${this.$proxyUrl}/playlist-api/v1/private/${this.username}`,
                    { headers: {"x-api-token": this.token} })
                    .then((response) => {
                        this.playlists = response.data.result;
                        if (this.$parent.selectedPlaylist === null) {
                            this.setPlaylistToParent(response.data.result[0])
                        }
                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },
            setPlaylistToParent: function (selectedPlayList) {
                this.$emit("setPlaylistToParent", selectedPlayList);
            },
            scrollTo: function (anchorPoint) {
                location.href = anchorPoint
            },
        },
        mounted() {
            if (this.loggedIn) {
                this.getAllUserPlaylists()
            }
            else {
                this.getAllPlaylists()
            }
            if (typeof this.$route.params.playlist !== 'undefined') {
                this.setPlaylistToParent(this.$route.params.playlist)
                this.scrollTo("#main")
            }

        },
        components: {
            Carousel,
            Slide,
        },
    }
</script>

<style scoped>

    .playlistselector {
        cursor: pointer;
        margin: 0 0 2em 0;
    }

    .image {
        position: relative;
        display: inline-block;
        border: 0;
        outline: 0;
    }

    .image img {
        display: block;
        width: 100%;
    }

    .image.featured {
        display: block;
        width: 100%;
        margin: 0 0 0 0;
        cursor: pointer;
    }

    ul {
        list-style-type: none;
    }


    .VueCarousel-slide {
        display: inline-block;
        width: 80%;
        height: 45em;
        background: #FF9B0D;
        border-style: solid;
        border-width: 2em;
        border-color: #ffffff;
        text-align: center;
        white-space: normal;
        overflow: auto;
        opacity: 1;
        -moz-transition: opacity 0.75s ease-in-out;
        -webkit-transition: opacity 0.75s ease-in-out;
        -ms-transition: opacity 0.75s ease-in-out;
        transition: opacity 0.75s ease-in-out;
    }

    @media screen and (max-width: 412px) {
        .VueCarousel-slide {
            height: 35em;
        }
    }

    .label {
        position: relative;
        top: 0;
        width: auto;
    }

    .label .image {
        position: relative;
        width: auto;
        margin-bottom: 1em;
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
        color: #7A2F9E;
    }


</style>
