<template>
    <!-- Home -->
    <div id="header" class="toppage">
        <header>
            <h1 id="logo">The Beverage Randomizer</h1>
            <p>Let fate quench your thirst!</p>
        </header>
        <footer>
            <a href="#playlistCarousel" class="letsGetStartedButton" v-smooth-scroll="{ duration: 1500 }" id="letsGetStartedButton"><strong>Let's Go!</strong></a>
        </footer>
    </div>
</template>

<script>
    export default {
        name: "Banner",
        data () {
            return {}
        },
    }
</script>

<style scoped>

    #header {
        position: relative;
        background-image: url("../assets/images/header02.jpg");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: #fff;
        text-align: center;
        padding: 7.5em 0 2em 0;
        cursor: default;
        opacity: 0.9;
    }

    #header .inner {
        position: relative;
        z-index: 1;
        margin: 0;
        display: inline-block;
        vertical-align: middle;
    }

    #header header {
        display: inline-block;
    }

    h1 {
        font-weight: bold;
        margin-top: 0.5em;
        margin-bottom: 1em;
        font-size: 2em;
        text-align: center;
    }

    .letsGetStartedButton {
        margin:0 auto;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #FF9500;
        color: #FFFFFF;
        text-align: center;
        width: 5em;
        height: 5em;
        border-radius: 100%;
        text-decoration: none;
        cursor: pointer;
        outline: 0;
        font-weight: 400;
    }

</style>
