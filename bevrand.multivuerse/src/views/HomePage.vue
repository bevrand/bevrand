<template>
    <div>
    <navbar></navbar>
    <banner></banner>
    <landingarea></landingarea>
    <playlistselection></playlistselection>
    <randomizer></randomizer>
    <foot></foot>
    <router-view @selectedPlaylist="setPlayList" />
    </div>
</template>

<script>
    import LandingArea from '../components/LandingArea.vue'
    import Banner from '../components/Banner.vue'
    import PlaylistSelection from '../components/PlaylistSelection.vue'
    import Randomizer from '../components/Randomizer.vue'
    import Footer from '../components/Footer.vue'
    import Navbar from "../components/Navbar";

    export default {
        name: 'homepage',
        data () {
            return {
                selectedPlaylist: null,
                selectedPlaylistText: "select playlist"
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
                console.log(playlist)
                this.selectedPlaylist = playlist;
                this.selectedPlaylistText = playlist;
            }
        },
        computed: {
        },
    }
</script>