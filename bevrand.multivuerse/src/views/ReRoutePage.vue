<template>
    <div id="readablemain">
    <navbar></navbar>
        <section class="reroute">
        <h2>{{username}}, your adventure starts here!</h2>
            <fulfilling-square-spinner v-if="animate"
                    :animation-duration="1200"
                    :size="100"
                    :color="'#fff'"
                    class="spinner"
            />
        <p>We wil be rerouting you to your Profile in: {{count}} seconds</p>
        </section>
    <foot></foot>
    </div>
</template>

<script>
import Footer from "../components/Footer.vue"
import Navbar from "../components/Navbar.vue"
import { FulfillingSquareSpinner } from 'epic-spinners'

    export default {
        name: 'reroutePage',
        data() {
            return {
                username: this.$route.params.username,
                count: 3,
                animate: false
            };
        },

        created() {
            this.animate = true;
            this.reRouteToProfile()

        },

        components: {
            'navbar': Navbar,
            'foot': Footer,
            FulfillingSquareSpinner,
        },

        methods: {
            reRouteToProfile : function () {
                window.setInterval(() => {
                    if (this.count === 0) {
                        this.$router.push({ name: 'profilePage'  });
                    }
                    this.count--;
                }, 1000);
            },
        }
    };
</script>

<style scoped>
    #readablemain {
        background-color: #7C7C7C;
        text-align: center;
    }

    .reroute {
        text-align: center;
        height: 25em;
    }

    .reroute p {
        text-align: center;
        font-size: 1.5em;
    }

    @media screen and (max-width: 650px) {
        .reroute p {
            font-size: 1em;
        }
    }

    @media screen and (max-width: 1366px) {
        .reroute {
            margin-top: 2em;
            margin-left: 10em;
            margin-right: 10em;
            text-align: center;
        }
    }

    @media screen and (max-width: 650px) {
        .reroute {
            margin-top: 2em;
            margin-left: 1em;
            margin-right: 1em;
            text-align: center;
            font-size: 1em;
        }
    }

    h2 {
        font-weight: bold;
        margin-top: 1em;
        font-size: 2em;
        text-align: center;
    }

    .spinner {
        margin-top: 8em;
        margin-bottom: 4em;
        margin-left: 45%;
        text-align: center;
    }

    @media screen and (max-width: 1366px) {
        .spinner {
            margin: 5em 10em 3em 35%;
            text-align: center;
        }
    }

    @media screen and (max-width: 650px) {
        .spinner {
            margin: 3em 1em 2em 38%;
            text-align: center;
        }
    }
</style>