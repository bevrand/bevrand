<template>
    <!-- Carousel -->
        <carousel :perPageCustom="[[320, 1], [768, 2], [1024, 3]]"
                  :loop="true"
                  :mouseDrag="true" id="playlistCarousel">
            <slide v-for="playlist of playlists">
                <span class="label">
                <a class="image featured" href="#main" v-smooth-scroll="{ duration: 1000 }" v-on:click="setPlaylistToParent(playlist)"><img :src="playlist.imageUrl" ></a>
                <a class="playlistselector" href="#main" v-smooth-scroll="{ duration: 1000 }" v-on:click="setPlaylistToParent(playlist)" id="playlistName"><h3>{{ playlist.displayName }}</h3>  </a>
                <ul id="beverageList">
                    <li v-for="beverage of playlist.beverages" >
                        {{ beverage }}
                    </li>
                </ul>
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
            }
        },
        created() {

        },
        methods: {
            getAllPlaylists: function () {
                this.$apiClient.get("http://0.0.0.0:4540/api/v2/frontpage")
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
            setPlaylistToParent: function (selectedPlayList) {
                this.$emit("setPlaylistToParent", selectedPlayList);
            },

        },
        mounted() {
            this.getAllPlaylists()
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
        background: #FF9B0D;
        border-style: solid;
        border-width: 2em;
        border-color: #ffffff;
        text-align: center;
        white-space: normal;
        height: 35em;
        overflow: auto;
        opacity: 1;
        -moz-transition: opacity 0.75s ease-in-out;
        -webkit-transition: opacity 0.75s ease-in-out;
        -ms-transition: opacity 0.75s ease-in-out;
        transition: opacity 0.75s ease-in-out;
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


</style>