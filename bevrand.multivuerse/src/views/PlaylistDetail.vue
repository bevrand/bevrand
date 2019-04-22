<template>
    <div id="playlistDetaild" class="playlistcreation">
        <navbar></navbar>
        <div id="creationArea" class="creationfield">
            <span class="label">
                <a class="image featured" ><img :src="imageUrl" ></a><br>
                <a class="playlistselector" id="playlistName"><h3> Playlist: {{ displayName }}</h3>  </a>
                <h3 style="margin-bottom: 0.5em">Beverages:</h3><br>
                <ul id="beverageList">
                    <li v-for="beverage of beverages" >
                        {{ beverage }}
                    </li>
                    <li>
                    <router-link
                            tag="button"
                            id="linkToAllDrinks"
                            class="showAllButton"
                            :to="{ name: 'homepage'}">
                    Sure now Randomize!
                    </router-link>
                    </li>
                </ul>
            </span>
        <foot></foot>
    </div>
    </div>
</template>


<script>
    import Footer from "../components/Footer.vue"
    import Navbar from "../components/Navbar.vue"

    export default {
        name: 'PlaylistDetail',
        data() {
            return {
                displayName: this.$route.params.playlistDetail.displayName,
                beverages:this.$route.params.playlistDetail.beverages,
                imageUrl: this.$route.params.playlistDetail.imageUrl,
            };
        },
        mounted() {
            this.normalizeName();
        },
        created() {
        },

        components: {
            'navbar': Navbar,
            'foot': Footer,
        },
        methods: {
            normalizeName: function () {
                this.normalizedPlayListName = this.displayName.replace(/[^a-zA-Z0-9]/g, "")
                    .toLowerCase();
            },

            setImage() {
                this.$swal({
                    text: 'Enter an image url',
                    content: "input",
                    placeholder: "Image url",
                    buttons: {
                        cancel: true,
                        confirm: {
                            text: "Change!",
                            closeModal: true,
                        },
                    },
                })
                    .then(value => {
                        if (value == null) {
                            this.$swal.stopLoading();
                            this.$swal.close()
                        }
                        else if (value.trim() === '') {
                            this.$swal('Value cannot be empty').then(() => {
                                this.setImage()
                            })
                        }
                        else {
                            this.$swal("Validation", "Changed image url", "success").then(() => {
                                this.imageUrl = value;
                            });
                        }
                    })},
            addBeverage : function () {
                let normalizedDrink = this.drink.charAt(0).toUpperCase() + this.drink.slice(1);
                if (this.beverages.indexOf(normalizedDrink) > -1){
                    this.$swal('Selected drink is already in this playlist')
                }
                else if (normalizedDrink.length < 2 || normalizedDrink.trim() === '') {
                    this.$swal('Drink is too short or empty')
                }
                else {
                    this.beverages.push(normalizedDrink);
                    this.drink = ''
                }

            },
            removeDrink (index) {
                this.beverages.splice(index, 1)
            },
            editDrink (index) {
                this.$swal({
                    text: 'Enter a new name',
                    content: "input",
                    placeholder: "Beer",
                    buttons: {
                        cancel: true,
                        confirm: {
                            text: "Change",
                            closeModal: true,
                        },
                    },
                })
                    .then(value => {
                        if (value == null) {
                            this.$swal.stopLoading();
                            this.$swal.close()
                        }
                        else if (value.trim() === '') {
                            this.$swal('Drink is too short or empty')
                        }
                        else {
                            this.drink = value;
                            this.addBeverage();
                            if(this.drink === '') {
                                this.$swal("Validation", `Changed ${this.beverages[index]} to ${value}`, "success");
                                this.removeDrink(index);
                            }
                        }
                    })},
            createNewPlaylist () {
                this.$apiClient({
                    method: "post",
                    url: `${this.$proxyUrl}/api/user`,
                    data: {
                        "beverages": this.beverages,
                        "displayName": this.displayName,
                        "imageUrl": this.imageUrl,
                        "list": this.normalizedPlayListName,
                        "user": this.username
                    }})
                    .then(response => {
                        this.$swal("Well done", `Playlist ${this.displayName} has been created`, "success").then(() => {
                            this.$router.push({ name: 'profilePage' });
                        });
                    })
                    .catch(e => {
                        this.$swal("Error", "Something went wrong", "error")
                    })
            },
            setPopularDrink (beverage) {
                if (this.beverages.indexOf(beverage) > -1){
                    this.$swal('Selected drink is already in this playlist')
                }
                else {
                    this.beverages.push(beverage);
                }
                this.expandPopularCocktails = false;
                this.expandPopularBeer = false;
                this.expandPopularWhiskey = false;
            },

            showPopularCockails () {
                this.expandPopularCocktails = !this.expandPopularCocktails;
                this.expandPopularBeer = false;
                this.expandPopularWhiskey = false;
            },
            showPopularBeers () {
                this.expandPopularBeer = !this.expandPopularBeer;
                this.expandPopularCocktails = false;
                this.expandPopularWhiskey = false;
            },
            showPopularWhiskeys () {
                this.expandPopularWhiskey = !this.expandPopularWhiskey;
                this.expandPopularBeer = false;
                this.expandPopularCocktails = false;
            }
        },
    };
</script>

<style scoped>
    .playlistcreation {
        background-color: #7A2F9E;
        text-align: center;
    }

    .image {
        position: relative;
        display: inline-block;
        border: 0;
        outline: 0;
    }

    .image img {
        display: block;
        width: 40%;
        height: 40%;
    }

    .image.featured {
        display: block;
        margin: 0 0 0 0;
        cursor: pointer;
    }

    ul {
        list-style-type: none;
    }

    .label {
        position: relative;
        top: 0;
        width: auto;
    }

    .label .image {
        position: relative;
        width: 65%;
        height: auto;
        margin-top: 2em;
        margin-left: 37%;
        margin-bottom: 1em;
    }

    @media screen and (max-width: 1366px) {
        .label .image {
            position: relative;
            width: 75%;
            height: auto;
            margin-top: 2em;
            margin-left: 30%;
            margin-bottom: 0.5em;
        }
    }

    @media screen and (max-width: 650px) {
        .label .image {
            position: relative;
            margin-top: 1em;
            margin-left: 30%;
            margin-bottom: 0.25em;
        }
    }

    .label h3 {
        margin-bottom: 1em;
        font-size: 1.5em;
        cursor: pointer;
        font-weight: bold;
        text-align: center;
    }

    .hover-add {
        margin-left: 1em;
    }

    .hover-add:hover {
        color: #68ff27;
    }

    .hover-popular {
        color: #ff9500;
    }

    .hover-delete {
        margin-left: 0.5em;
    }

    .hover-delete:hover {
        color: #ff271a;
    }

    .hover-edit {
        margin-left: 0.5em;
    }

    .hover-edit:hover {
        color: #3cfaff;
    }

    .adddrink {
        margin-bottom: 2em;
        font-family: "Ubuntu", sans-serif;
    }

    .circledbutton{
        position: relative;
        height: 3em;
        margin-left: 0.5em;
        margin-bottom: 0.5em;
        width: 12em;
        font-size:13px;
        font-family:arial, helvetica, sans-serif;
        padding: 10px 10px 10px 10px;
        text-shadow: -1px -1px 0 rgba(0,0,0,0.3);
        font-weight:bold;
        text-align: center;
        color: #FFFFFF;
        background-color: #FF9500;
    }

    .circledbutton:hover{
        background: #7A2F9E;
    }

    .submitbutton {
        position: relative;
        display: inline-block;
        background: #ff9500;
        color: #ffffff;
        text-align: center;
        border-radius: 0.5em;
        text-decoration: none;
        padding: 0.65em 3em 0.65em 3em;
        margin-top: 2em;
        margin-bottom: 2em;
        cursor: pointer;
        outline: 0;
        font-weight: 400;
        font-size: 1em;
        font-family: "Ubuntu", sans-serif;
        -moz-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
        -webkit-transition: background-color 0.35s ease-in-out,
        color 0.35s ease-in-out, border-bottom-color 0.35s ease-in-out;
        -ms-transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
        transition: background-color 0.35s ease-in-out, color 0.35s ease-in-out,
        border-bottom-color 0.35s ease-in-out;
    }

    .submitbutton:hover {
        color: #fff;
        background: #424242;
        letter-spacing: 1px;
        -webkit-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
        -moz-box-shadow: 0px 5px 40px -10px rgba(0, 0, 0, 0.57);
        box-shadow: 5px 40px -10px rgba(0, 0, 0, 0.57);
        transition: all 0.4s ease 0s;
    }

</style>

