<template>
    <div id="landingarea">
        <!-- Inner -->
        <div class="banner">
            <header>
                <h1 id="logo">The Beverage Randomizer</h1>
                <hr />
                <p>Let fate quench your thirst!</p>
            </header>
            <footer>
                <a href="#main" class="button circled scrolly" id="letsGetStartedButton"><strong>Let's Go!</strong></a>
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