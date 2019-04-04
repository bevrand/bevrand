<template>
    <div id="readablemain">
        <navbar></navbar>
        <loginarea></loginarea>
        <foot></foot>
    </div>
</template>

<script>
import Footer from "../components/Footer.vue"
import Navbar from "../components/Navbar.vue"
import Login from "../components/LoginArea.vue"

export default {
        name: "login",
        data () {
            return {}
        },

        components: {
            'navbar': Navbar,
            'loginarea': Login,
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