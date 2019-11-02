<template>
    <div id="picturesUploadArea" class="pictureupload">
        <navbar></navbar>
        <div class="banner">
            <p>
            <h1>Want to randomize from your favourite menu? </h1><br>
                <strong>Step 1:</strong> Take a picture of the menu items you would like to upload <br>
                <strong>Step 2:</strong> Review picture in the preview (this might be cropped)<br>
                <strong>Step 3:</strong> Upload image using the <button class="randomizeButtonIcon"></button> upload button <br>
                <strong>Step 4:</strong> Remove any unwanted suggestions using the <font-awesome-icon icon="trash" size="s"/> icon<br>
                <strong>Step 5:</strong> Add these beverages to your playlist<br>
            </p>
        </div>
        <h2>Preview:</h2><br>
        <picture-input
                ref="pictureInput"
                @change="onChange"
                width="600"
                height="1000"
                margin="8"
                accept="image/jpeg,image/png"
                size="12"
                :hideChangeButton="true"
                :customStrings="{
                        drag: 'Select a JPEG or PNG'
                    }">
        </picture-input>
        <br><br>
        <circles-to-rhombuses-spinner v-if="uploading"
                                      :animation-duration="1200"
                                      :circles-num="4"
                                      :circle-size="15"
                                      color="#ff9500"
                                      class="spinner"
        />
        <button class="randomizeButton" v-on:click="uploadImage()" v-if="!uploading">Upload Image</button>
        <ul id="drinksFromPicture" v-if="!uploading">
            <li v-for="(beverage, index) in drinksFromPicture" :key="index" >
                {{ beverage }}
                <a class="hover-delete">
                    <font-awesome-icon icon="trash" class="icons" v-on:click="removeDrink(index)" />
                </a>
            </li>
        </ul>
        <ul id="drinkToAdd" v-if="drinksFromPicture.length > 0 && !uploading">
            <button class="randomizeButton" v-on:click="sendDrinksToPlaylistCreation()" v-if="drinksFromPicture.length > 0 && !uploading">Add all beverages</button>
        </ul>
        <foot></foot>
    </div>
</template>

<script>
import Footer from "../components/Footer.vue"
import Navbar from "../components/Navbar.vue"
import PictureInput from 'vue-picture-input'
import { CirclesToRhombusesSpinner } from 'epic-spinners'

    export default {
        name: 'Pictures',
        data () {
            return {
                displayName: this.$store.state.creationPlaylistDisplayname,
                token: this.$store.state.token,
                image: '',
                drinksFromPicture: '',
                errors: '',
                uploading: false,
                count: 5
            }
        },
        components: {
            PictureInput,
            CirclesToRhombusesSpinner,
            'navbar': Navbar,
            'foot': Footer,
        },
        methods: {
            onChange (image) {
                if (image) {
                    this.image = image
                }
            },
            uploadImage () {
                this.count = 5;
                this.uploading = true;
                this.$apiClient({
                    method: 'post',
                    url: `${this.$proxyUrl}/ocr-api/v1/base64`,
                    data: {'base64': this.image},
                    headers: {"x-api-token": this.token}
                })
                    .then((response) => {
                        window.setInterval(() => {
                            if (this.count === 0) {
                                this.uploading = false;
                            }
                            this.count--;
                        }, 1000);
                        this.drinksFromPicture = response.data['imageText'];
                    })
                    .catch(e => {
                        window.setInterval(() => {
                            if (this.count === 0) {
                                this.uploading = false;
                            }
                            this.count--;
                        }, 1000);
                        this.errors.push(e)
                    })
            },
            removeDrink (index) {
                this.drinksFromPicture.splice(index, 1)
            },
            sendDrinksToPlaylistCreation : function () {
                this.$store.commit('setDrinksFromPicture', this.drinksFromPicture);
                this.$router.push({ name: 'playlistCreationPage', params: { displayName: this.displayName} })
            }
        }
    }
</script>

<style scoped>
    .pictureupload {
        background-color: #7A2F9E;
        text-align: center;
    }

    h1 {
        font-weight: normal;
        font-size: 2em;
    }

    h2 {
        font-weight: normal;
        font-size: 1.5em;
    }

    ul {
        list-style-type: none;
    }

    a {
        color: #ffffff;
    }

    p {
        text-align: center;
    }

    .randomizedtext {
        font-weight: bold;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        font-size: 1.5em;
        text-align: center;

    }

    .randomizeButton {
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

    .randomizeButtonIcon {
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


    .randomizeButton:hover {
        color: #fff;
        background: #7A2F9E;
        letter-spacing: 1px;
        -webkit-box-shadow: 0px 5px 40px -10px rgba(0,0,0,0.57);
        -moz-box-shadow: 0px 5px 40px -10px rgba(0,0,0,0.57);
        box-shadow: 5px 40px -10px rgba(0,0,0,0.57);
        transition: all 0.4s ease 0s;
    }

    .hover-add {
        margin-left: 1em;
    }

    .hover-add:hover {
        color: #68ff27;
    }

    .hover-delete {
        margin-left: 0.5em;
    }

    .hover-delete:hover {
        color: #ff271a;
    }

</style>