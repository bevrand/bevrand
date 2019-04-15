<template>
    <div id="readablemain">
        <navbar></navbar>
        <playlist></playlist>
        <foot></foot>
    </div>
</template>

<script>
    import Footer from '../components/Footer.vue'
    import Navbar from "../components/Navbar.vue"
    import PlayListCreation from "../components/ProfileArea.vue"

    export default {
        name: "profile",
        data () {
            return {
            }
        },

        components: {
            'navbar': Navbar,
            'foot': Footer,
            'playlist': PlayListCreation,
        },
    }
</script>

<style scoped>
    #readablemain {
        background-color: #7C7C7C;
        text-align: center;
    }
</style>