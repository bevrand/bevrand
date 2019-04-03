<template>
    <!-- Home -->
    <div id="top" class="toppage">
        <header>
            <p>
                All those Beverage choices bringing you down? Feeling lucky? <br>
                Choose a list below, click Randomize and let fate decide!
            </p>
        </header>
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

    .toppage {
        box-shadow: inset 0px 1px 0px 0px rgba(0, 0, 0, 0.05), inset 0px 2px 3px 0px rgba(0, 0, 0, 0.1);
        padding: 8em 0 8em 0;
        text-align: center;
        height: 40em;
        position: relative;
        background-image: url("../assets/images/header02.jpg");
        opacity: 0.9;
    }

    .toppage::after {
        background-image: url("../assets/images/header02.jpg");
        opacity: 0.9;
        position: absolute;
        content: "";
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }

    .image {
        display: inline-block;
        position: relative;
        height: 25%;
        width: 25%;
    }
</style>
