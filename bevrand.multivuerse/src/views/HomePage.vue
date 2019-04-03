<template>
    <div id="homepage">
    <navbar></navbar>
    <banner></banner>
    <landingarea></landingarea>
    <playlistselection v-on:setPlaylistToParent="setPlayList"></playlistselection>
    <randomizer></randomizer>
    <foot></foot>
    </div>
</template>

<script>
    import LandingArea from '../components/LandingArea.vue'
    import Banner from '../components/Banner.vue'
    import PlaylistSelection from '../components/PlaylistSelection.vue'
    import Randomizer from '../components/Randomizer.vue'
    import Footer from '../components/Footer.vue'
    import Navbar from "../components/Navbar.vue";

    export default {
        name: 'homepage',
        data () {
            return {
                selectedPlaylist: null,
                selectedPlaylistDisplayName: "select playlist"
            }
        },

        components: {
            'navbar': Navbar,
            'banner': Banner,
            'landingarea': LandingArea,
            'playlistselection' : PlaylistSelection,
            'randomizer' : Randomizer,
            'foot': Footer
        },
        methods: {
            setPlayList(playlist) {
                this.selectedPlaylist = playlist;
                this.selectedPlaylistDisplayName = playlist['displayName'];
            },
        },
        computed: {
        },
    }
</script>

<style scoped>
    #homepage {
        background-color: #ffffff;
    }
</style>