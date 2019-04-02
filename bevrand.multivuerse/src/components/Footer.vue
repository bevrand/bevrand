<template>
    <!-- Footer -->
    <div id="footer" class="footer">
            <header>
                <h3>Wanna reach out?</h3>
            </header>
            <p>Our project is open source so feel free to clone from our github.</p>
            <a href="https://www.github.com/bevrand/bevrand" class="icon fa-github"><span class="label">Github</span></a>
        <!-- Copyright -->
        <div class="copyright">
            <a>&copy; Copyright (c) 2017 bevrand</a><br>
            <a>Beverage Randomizer</a>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Footer",
        data () {
            return {}
        },
    }
</script>

<style scoped>
    #footer {
        position: relative;
        overflow: hidden;
        padding: 6em 0 6em 0;
        background: #424242;
        color: #fff;
    }

    #footer .icon.circled {
        background: #fff;
        color: #2b252c;
    }

    #footer header {
        text-align: center;
        cursor: default;
    }

    #footer .contact {
        text-align: center;
    }

    #footer .contact p {
        text-align: center;
        margin: 0 0 3em 0;
    }

    #footer .copyright {
        text-align: center;
        color: rgba(128, 128, 128, 0.75);
        font-size: 0.8em;
        cursor: default;
    }

    #footer .copyright a:hover {
        color: rgba(212, 212, 212, 0.85);
    }


</style>