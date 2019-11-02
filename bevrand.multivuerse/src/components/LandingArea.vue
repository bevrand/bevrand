<template>
    <div id="landingarea">
        <!-- Inner -->
        <div class="banner">
            <p>
                All those Beverage choices bringing you down? <br>
                Let fate decide!
                <br>
                <br>
                <br>
                <strong>Step 1:</strong> Press the dice <font-awesome-icon icon="dice" class="icons" size="1x"/> to select a playlist <br>
                <strong>Step 2:</strong> Press the <button class="randomizeButton"></button> to randomize<br>
                <strong>Step 3:</strong> Drink up! <br>
            </p>

            <a id="scrollToPlaylists" href="#playlistCarousel" v-smooth-scroll="{ duration: 1000 }"><font-awesome-icon  icon="arrow-alt-circle-down" class="icons" size="3x"/></a>
        </div>
    </div>

</template>

<script>
    export default {
        name: "LandingArea",
        data () {
            return {}
        },
    }
</script>

<style scoped>

    .banner {
        background: #7A2F9E;
        text-align: center;
        padding: 4.5em 1em 4.5em 1em;
        margin-bottom: 0;
    }

    #landingarea p {
        margin-bottom: 1em;
        font-size: 1.5em;
        text-align: center;
    }

    .randomizeButton {
        display: inline;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: #FF9500;
        color: #FFFFFF;
        text-align: center;
        width: 3em;
        height: 3em;
        border-radius: 100%;
    }

</style>