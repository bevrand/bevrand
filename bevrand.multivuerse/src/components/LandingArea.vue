<template>
    <div id="landingarea">
        <!-- Inner -->
        <div class="banner">
            <p>
                All those Beverage choices bringing you down? <br>
                Choose a playlist below, click Randomize and let fate decide!
            </p>
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

</style>