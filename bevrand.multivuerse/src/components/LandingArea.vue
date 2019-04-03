<template>
    <div id="landingarea">
        <!-- Inner -->
        <div class="banner">
            <header>
                <h1 id="logo">The Beverage Randomizer</h1>
                <p>Let fate quench your thirst!</p>
            </header>
            <footer>
                <a href="#main" class="letsGetStartedButton" v-smooth-scroll="{ duration: 1500 }" id="letsGetStartedButton"><strong>Let's Go!</strong></a>
            </footer>
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

    h1 {
        font-weight: bold;
        margin-top: 0.5em;
        margin-bottom: 1em;
        font-size: 3.5em;
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
        width: 7em;
        height: 7em;
        border-radius: 100%;
        text-decoration: none;
        cursor: pointer;
        outline: 0;
        font-weight: 400;
    }

    .banner {
        background: #7A2F9E;
        text-align: center;
        padding: 4.5em 0 4.5em 0;
        margin-bottom: 0;
    }

    .banner header>p {
        margin-bottom: 0;
    }
</style>