<template>
    <!-- Main -->
    <div class="wrapper style2">
        <div id="main" class="container special">
            <h3 class="playlisttext" id="currentlySelectedPlayList"> {{$parent.selectedPlaylistText}} </h3>
            <div class="container style2">
                <div class="pour"></div>
                <div id="beaker">
                    <div class="beer-foam">
                        <div class="foam-1"></div>
                        <div class="foam-2"></div>
                        <div class="foam-3"></div>
                        <div class="foam-4"></div>
                        <div class="foam-5"></div>
                        <div class="foam-6"></div>
                        <div class="foam-7"></div>
                    </div>

                    <div id="liquid">
                        <div class="bubble bubble1"></div>
                        <div class="bubble bubble2"></div>
                        <div class="bubble bubble3"></div>
                        <div class="bubble bubble4"></div>
                        <div class="bubble bubble5"></div>
                    </div>
                </div>
            </div>
            <h2 id="randomizedDrink" v-if="!isHidden">{{drink}}</h2>
            <a class="randomizeButton" v-if="!isHidden" id="randomizebutton" v-on:click="randomizeDrink"><strong>Randomize!</strong></a>
        </div>
    </div>
</template>

<script>
import JQuery from 'jquery'
let $ = JQuery;

    export default {
        name: "Randomizer",
        data() {
            return {
                isHidden: false,
                drink: "Press Randomize Button!"
            }
        },
        methods: {
            randomizeDrink: function() {
            this.isHidden = true;
            $('.pour').css({
                height: '0px',
                marginTop: '0px'});

            $('.pour') // Start pouring down
                .animate({
                    height: '360px'
                }, 2500)
                .slideDown(500);

            $('#liquid') // Lower liquid level
                .animate({
                    height: '-10px'
                }, 1200);

            $('.beer-foam') // Lower beer foam
                .animate({
                    bottom: '20px'
                }, 1000);

            $('#liquid') // I Said Fill 'Er Up!
                .delay(1000)
                .animate({
                    height: '200px'
                }, 2000);

            $('.beer-foam') // Keep that Foam Rollin' Toward the Top! Yahooo!
                .delay(1000)
                .animate({
                    bottom: '200px'
                }, 2400);

            $('.pour') // Stop pouring beer
                .animate({
                    height: '0px',
                    marginTop: '360px'
                }, 1500)
                //.delay(1600)
                .slideUp(500);

                setTimeout(function(){
                    self.isHidden = false;
                }, 4500);
        },

        randomize: function () {
            axios.get("http://0.0.0.0:4540/api/v2/randomize")
                .then((response) => {
                    this.playlists = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        setPlaylist: function (displayName) {
            this.$emit("selectedPlaylist", displayName);
        }
    }
}
</script>

<style scoped>

    .playlisttext {
        margin-top: 5em;
        margin-bottom: 20px;
        text-align: center;
        font-weight: 400;
    }

    .randomizeButton {
        position: center;
        display: inline-block;
        background: #FF9500;
        color: #FFFFFF;
        text-align: center;
        border-radius: 0.5em;
        text-decoration: none;
        padding: 0.65em 3em 0.65em 3em;
        cursor: pointer;
        outline: 0;
        font-weight: 400;
        -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -webkit-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
    }
    /* Main */

    #main {
        margin-bottom: 0;
    }

    #main section:first-of-type {
        padding-top: 2em;
    }

    .container.style2 {
        height: 370px;
        margin: 0 auto;
        overflow: hidden;
        position: relative;
        top: -20px;
        width: 248px;
    }

    .container.style2 div {
        position: absolute;
    }

    .pour {
        position: absolute;
        left: 45%;
        width: 20px;
        height: 0;
        background-color: #edaf32;
        border-radius: 10px
    }

    #beaker {
        border: 10px solid #FFF;
        border-top: 0;
        border-radius: 0 0 30px 30px;
        height: 200px;
        left: 14px;
        bottom: 0;
        width: 220px;
    }

    #beaker:before,
    #beaker:after {
        border: 10px solid #FFF;
        border-bottom: 0;
        border-radius: 30px 30px 0 0;
        content: '';
        height: 30px;
        position: absolute;
        top: -30px;
        width: 50px;
    }

    #beaker:before {
        left: -50px;
    }

    #beaker:after {
        right: -50px;
    }

    #liquid {
        background-color: #edaf32;
        border: 10px solid #edaf32;
        border-radius: 0 0 20px 20px;
        bottom: 0;
        height: 0;
        overflow: hidden;
        width: 200px;
    }

    #liquid:after {
        background-color: rgba(255, 255, 255, 0.25);
        bottom: -10px;
        content: '';
        height: 200px;
        left: -40px;
        position: absolute;
        transform: rotate(30deg);
        -webkit-transform: rotate(15deg);
        width: 110px;
    }

    #liquid .bubble {
        -webkit-animation-name: bubble;
        -webkit-animation-iteration-count: infinite;
        -webkit-animation-timing-function: linear;
        background-color: rgba(255, 255, 255, 0.2);
        bottom: 0;
        border-radius: 10px;
        height: 20px;
        width: 20px;
    }

    @-webkit-keyframes bubble {
        0% {
            bottom: 0;
        }
        50% {
            background-color: rgba(255, 255, 255, 0.2);
            bottom: 80px;
        }
        100% {
            background-color: rgba(255, 255, 255, 0);
            bottom: 160px;
        }
    }

    .bubble1 {
        left: 10px;
        animation-delay: 1000 ms;
        -webkit-animation-delay: 1000ms;
        -webkit-animation-duration: 1000ms;
    }

    .bubble2 {
        left: 50px;
        -webkit-animation-delay: 700ms;
        -webkit-animation-duration: 1100ms;
    }

    .bubble3 {
        left: 100px;
        -webkit-animation-delay: 1200ms;
        -webkit-animation-duration: 1300ms;
    }

    .bubble4 {
        left: 130px;
        -webkit-animation-delay: 1100ms;
        -webkit-animation-duration: 700ms;
    }

    .bubble5 {
        left: 170px;
        -webkit-animation-delay: 1300ms;
        -webkit-animation-duration: 800ms;
    }


    /* Foam */

    .beer-foam {
        position: absolute;
        bottom: 10px;
    }

    .foam-1,
    .foam-2,
    .foam-3,
    .foam-4,
    .foam-5,
    .foam-6,
    .foam-7 {
        float: left;
        position: absolute;
        z-index: 998;
        width: 50px;
        height: 50px;
        border-radius: 30px;
        background-color: #fefefe;
    }

    .foam-1 {
        top: -30px;
        left: -10px;
    }

    .foam-2 {
        top: -35px;
        left: 20px;
    }

    .foam-3 {
        top: -25px;
        left: 50px;
    }

    .foam-4 {
        top: -35px;
        left: 80px;
    }

    .foam-5 {
        top: -30px;
        left: 110px;
    }

    .foam-6 {
        top: -20px;
        left: 140px;
    }

    .foam-7 {
        top: -30px;
        left: 160px;
    }


    /* Drunk Text */

    .animated {
        -webkit-animation-fill-mode: both;
        -moz-animation-fill-mode: both;
        animation-fill-mode: both;
        -webkit-animation-duration: 5s;
        -moz-animation-duration: 5s;
        animation-duration: 5s;
        -webkit-animation-delay: 3.5s;
        -moz-animation-delay: 3.5s;
        animation-delay: 3.5s;
    }

    .animated.drunk {
        -webkit-animation-duration: 2s;
        -moz-animation-duration: 2s;
        animation-duration: 2s;
    }

    @-webkit-keyframes drunk {
        0% {
            -webkit-transform: rotate(0);
            -webkit-transform-origin: top left;
            -webkit-animation-timing-function: ease-in-out;
        }
        20%,
        60% {
            -webkit-transform: rotate(80deg);
            -webkit-transform-origin: top left;
            -webkit-animation-timing-function: ease-in-out;
        }
        40% {
            -webkit-transform: rotate(60deg);
            -webkit-transform-origin: top left;
            -webkit-animation-timing-function: ease-in-out;
        }
        80% {
            -webkit-transform: rotate(60deg) translateY(0);
            -webkit-transform-origin: top left;
            -webkit-animation-timing-function: ease-in-out;
            opacity: 1;
        }
        100% {
            -webkit-transform: translateY(700px);
            opacity: 0;
        }
    }

    @-moz-keyframes drunk {
        0% {
            -moz-transform: rotate(0);
            -moz-transform-origin: top left;
            -moz-animation-timing-function: ease-in-out;
        }
        20%,
        60% {
            -moz-transform: rotate(80deg);
            -moz-transform-origin: top left;
            -moz-animation-timing-function: ease-in-out;
        }
        40% {
            -moz-transform: rotate(60deg);
            -moz-transform-origin: top left;
            -moz-animation-timing-function: ease-in-out;
        }
        80% {
            opacity: 1;
            -moz-transform: rotate(60deg) translateY(0);
            -moz-transform-origin: top left;
            -moz-animation-timing-function: ease-in-out;
        }
        100% {
            -moz-transform: translateY(700px);
            opacity: 0;
        }
    }

    @keyframes drunk {
        0% {
            transform: rotate(0);
            transform-origin: top left;
            animation-timing-function: ease-in-out;
        }
        20%,
        60% {
            transform: rotate(80deg);
            transform-origin: top left;
            animation-timing-function: ease-in-out;
        }
        40% {
            transform: rotate(60deg);
            transform-origin: top left;
            animation-timing-function: ease-in-out;
        }
        80% {
            transform: rotate(60deg) translateY(0);
            opacity: 1;
            transform-origin: top left;
            animation-timing-function: ease-in-out;
        }
        100% {
            transform: translateY(700px);
            opacity: 0;
        }
    }

    .drunk {
        -webkit-animation-name: drunk;
        -moz-animation-name: drunk;
        animation-name: drunk;
    }

</style>