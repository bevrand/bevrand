<template>
    <div id="readablemain">
    <navbar></navbar>
    <registerarea></registerarea>
    <foot></foot>
    </div>
</template>

<script>
    import Footer from '../components/Footer.vue'
    import Navbar from "../components/Navbar.vue"
    import Register from "../components/RegisterArea.vue"

    export default {
        name: "register",
        data () {
            return {}
        },

        components: {
            'navbar': Navbar,
            'registerarea': Register,
            'foot': Footer
        },
    }
</script>

<style scoped>
    #readablemain {
        background-color: #7C7C7C;
        text-align: center;
    }
</style>