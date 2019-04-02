<template>
    <!-- Carousel -->
    <section class="carousel">
        <div class="reel" id="playlistCarousel">
            <article v-for="playlist of playlists">
                <a class="image featured" href="#main" @click='setPlaylist(playlist)'><img :src="playlist.imageUrl" :alt="playlistImageUrl" ></a>
                <h3><a class="playlistselector" href="#main" @click='setPlaylist(playlist)' id="playlistName"> {{ playlist.displayName }} </a></h3>
                <ul id="beverageList">
                    <li v-for="beverage of playlist.beverages" >
                        {{ beverage }}
                    </li>
                </ul>
            </article>
        </div>
        </section>
</template>

<script>
import axios from 'axios';

    export default {
        name: "PlaylistSelection",
        data() {
            return {
                playlists: [],
                errors: []
            }
        },
        created() {
            this.getAllPlaylists();
        },
        methods: {
            getAllPlaylists: function () {
                    axios.get("http://0.0.0.0:4540/api/v2/frontpage")
                        .then((response) => {
                            this.playlists = response.data;
                        })
                        .catch(e => {
                            this.errors.push(e)
                        })
                },
            setPlaylist: function (playlist) {
                console.log(playlist)
                this.$emit("selectedPlaylist", playlist['displayName']);
            }
        }
    }
</script>

<style scoped>

    /* Image */

    .playlistselector {
        cursor: pointer;
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
        margin: 0 0 4em 0;
        cursor: pointer;
    }

    ul {
        list-style-type: none;
    }

    .carousel {
        position: relative;
        overflow: hidden;
        padding: 2em 0 2em 0;
        margin-bottom: 0;
    }

    .carousel .forward,
    .carousel .backward {
        position: absolute;
        top: 50%;
        width: 6em;
        height: 12em;
        margin-top: -6em;
        cursor: pointer;
    }

    .carousel .forward:before,
    .carousel .backward:before {
        content: '';
        display: block;
        width: 6em;
        height: 6em;
        border-radius: 100%;
        background-color: rgba(72, 57, 73, 0.5);
        position: absolute;
        top: 50%;
        margin-top: -3em;
        -moz-transition: background-color 0.35s ease-in-out;
        -webkit-transition: background-color 0.35s ease-in-out;
        -o-transition: background-color 0.35s ease-in-out;
        -ms-transition: background-color 0.35s ease-in-out;
        transition: background-color 0.35s ease-in-out;
        -webkit-backface-visibility: hidden;
    }

    .carousel .forward:after,
    .carousel .backward:after {
        content: '';
        width: 3em;
        height: 3em;
        position: absolute;
        top: 50%;
        margin: -1.5em 0 0 0;
        background: url("../assets/images/arrow.svg") no-repeat center center;
    }

    .carousel .forward:hover:before,
    .carousel .backward:hover:before {
        background-color: rgba(239, 131, 118, 0.75);
    }

    .carousel .forward {
        right: 0;
    }

    .carousel .forward:before {
        right: -3em;
    }

    .carousel .forward:after {
        right: -0.25em;
    }

    .carousel .backward {
        left: 0;
    }

    .carousel .backward:before {
        left: -3em;
    }

    .carousel .backward:after {
        left: -0.25em;
        -moz-transform: scaleX(-1);
        -webkit-transform: scaleX(-1);
        -ms-transform: scaleX(-1);
        transform: scaleX(-1);
    }

    .carousel .reel {
        white-space: nowrap;
        position: relative;
        -webkit-overflow-scrolling: touch;
        padding: 0 2em 0 2em;
    }

    .carousel article {
        display: inline-block;
        width: 18em;
        background: #FF9B0D;
        text-align: center;
        padding: 0 1em 3em 1em;
        margin: 0 2em 0 0;
        white-space: normal;
        height: 25em;
        overflow: auto;
        opacity: 1;
        -moz-transition: opacity 0.75s ease-in-out;
        -webkit-transition: opacity 0.75s ease-in-out;
        -ms-transition: opacity 0.75s ease-in-out;
        transition: opacity 0.75s ease-in-out;
    }

    .carousel article.loading {
        opacity: 0;
    }

    .carousel article .image {
        position: relative;
        left: -1em;
        top: 0;
        width: auto;
        margin-right: -2em;
        margin-bottom: 3em;
    }

    .carousel article p {
        text-align: center;
    }

</style>